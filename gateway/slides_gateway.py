"""Sanrathi gateway <-> Sanrathi Slide Maker (Presenton fork).
Add to the Sanrathi FastAPI app:  app.include_router(slides_gateway.router)
Env: SLIDES_URL=http://127.0.0.1:5001  SLIDES_API_KEY=sk-presenton-...
     OLLAMA_URL=http://127.0.0.1:11434  OLLAMA_MODEL=qwen2.5:7b
"""
import json, os, tempfile
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from watermark import stamp          # watermark.py from this guide

SLIDES_URL = os.environ["SLIDES_URL"].rstrip("/")
HEADERS = {"Authorization": f"Bearer {os.environ['SLIDES_API_KEY']}"}
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
router = APIRouter(prefix="/v1/slides", tags=["slides"])


class TextToSlides(BaseModel):
    topic: str = Field(min_length=3, max_length=4000)
    n_slides: int = Field(8, ge=3, le=25)
    language: str = "English"          # "Hindi", "Telugu", ... also work
    template: str = "sanrathi-paper"
    export_as: str = Field("pptx", pattern="^(pptx|pdf)$")


class LectureToSlides(BaseModel):
    transcript: str = Field(min_length=200)
    title: str
    max_slides: int = Field(15, ge=3, le=40)
    template: str = "sanrathi-paper"
    export_as: str = Field("pptx", pattern="^(pptx|pdf)$")


async def _start_job(body: dict) -> dict:
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(f"{SLIDES_URL}/api/v1/ppt/presentation/generate/async",
                         json=body, headers=HEADERS)
    if r.status_code >= 400:
        raise HTTPException(502, f"Slide Maker error: {r.text[:300]}")
    return r.json()                        # {"id": task_id, "status": "pending", ...}


@router.post("/from-text")
async def from_text(req: TextToSlides):
    job = await _start_job({
        "content": req.topic, "n_slides": req.n_slides, "language": req.language,
        "template": req.template, "export_as": req.export_as,
        "tone": "educational", "verbosity": "standard",
    })
    # TODO: save (job["id"], student_id) in your DB so only the owner can fetch it
    return {"job_id": job["id"]}


SEGMENT_PROMPT = """You turn part of a classroom lecture transcript into slides.
Rules:
- Use ONLY facts said in the transcript. Never add outside facts.
- Each slide: a '# Heading' line, then 2-5 short bullet points.
- Max 80 words per slide. Keep technical terms exactly as the teacher said them.
- Hinglish/code-mixed speech: write the slide in clear English.
Return JSON: {{"slides": ["# ...", "# ..."]}} with at most {k} slides.

TRANSCRIPT PART:
{chunk}"""


async def _segment(transcript: str, max_slides: int) -> list[str]:
    words = transcript.split()
    chunks = [" ".join(words[i:i + 1200]) for i in range(0, len(words), 1200)]
    per_chunk = max(1, max_slides // len(chunks))
    slides: list[str] = []
    async with httpx.AsyncClient(timeout=300) as c:
        for chunk in chunks:
            r = await c.post(f"{OLLAMA_URL}/api/chat", json={
                "model": OLLAMA_MODEL, "stream": False, "format": "json",
                "think": False,
                "options": {"temperature": 0.2, "num_ctx": 8192},
                "messages": [{"role": "user", "content":
                              SEGMENT_PROMPT.format(k=per_chunk, chunk=chunk)}],
            })
            r.raise_for_status()
            try:
                slides += json.loads(r.json()["message"]["content"])["slides"]
            except (KeyError, ValueError):
                continue                   # skip a bad chunk instead of failing all
    return [s for s in slides if isinstance(s, str) and s.strip()][:max_slides]


@router.post("/from-lecture")
async def from_lecture(req: LectureToSlides):
    slides = await _segment(req.transcript, req.max_slides)
    if len(slides) < 2:
        raise HTTPException(422, "Could not build slides from this transcript")
    job = await _start_job({
        "content": "", "slides_markdown": [f"# {req.title}"] + slides,
        "include_title_slide": False, "template": req.template,
        "export_as": req.export_as, "tone": "educational",
    })
    return {"job_id": job["id"], "slides_planned": len(slides) + 1}


@router.get("/jobs/{job_id}")
async def job_status(job_id: str):
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(f"{SLIDES_URL}/api/v1/async-tasks/status/{job_id}",
                        headers=HEADERS)
    r.raise_for_status()
    t = r.json()
    return {"status": t["status"], "message": t.get("message"),
            "ready": t["status"] == "completed"}


@router.get("/jobs/{job_id}/download")
async def download(job_id: str):
    async with httpx.AsyncClient(timeout=120) as c:
        t = (await c.get(f"{SLIDES_URL}/api/v1/async-tasks/status/{job_id}",
                         headers=HEADERS)).json()
        if t["status"] != "completed":
            raise HTTPException(409, "Not ready yet")
        path = t["data"]["path"]            # e.g. /app_data/exports/<file>.pptx
        f = await c.get(f"{SLIDES_URL}{path}", headers=HEADERS)
        f.raise_for_status()
    suffix = ".pdf" if path.endswith(".pdf") else ".pptx"
    raw = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    raw.write(f.content); raw.close()
    out = raw.name
    is_premium = False   # TODO: read from the logged-in user's plan, never from the URL
    if not is_premium:
        out = raw.name.replace(suffix, f"-sanrathi{suffix}")
        stamp(raw.name, out)
    return FileResponse(out, filename=f"sanrathi-slides{suffix}")
