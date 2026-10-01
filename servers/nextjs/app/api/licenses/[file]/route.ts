// Added by Sanrathi, 2026: serves the Apache 2.0 LICENSE and the NOTICE file
// (third-party attributions) as plain text for the Open-source licenses page.
import { readFile } from "fs/promises";
import path from "path";
import { NextResponse } from "next/server";

const FILES: Record<string, string> = {
  notice: "NOTICE",
  license: "LICENSE",
};

export async function GET(
  _request: Request,
  context: { params: Promise<{ file: string }> }
) {
  const { file } = await context.params;
  const name = FILES[file];
  if (!name) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  // Next.js runs from servers/nextjs (repo) or /app/servers/nextjs (Docker);
  // LICENSE and NOTICE live at the repo / image root.
  try {
    const text = await readFile(path.resolve(process.cwd(), "../..", name), "utf-8");
    return new NextResponse(text, {
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  } catch {
    return NextResponse.json({ error: `${name} not found` }, { status: 404 });
  }
}
