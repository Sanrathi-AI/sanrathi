// Added by Sanrathi, 2026: Open-source licenses page (Apache 2.0 attribution).
import React from "react";

export const metadata = {
  title: "Open-source licenses | Sanrathi Slide Maker",
  description: "Open-source software and models used by Sanrathi Slide Maker",
};

const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <section className="border-b border-[#EDEEEF] py-6">
    <h2 className="font-syne text-lg font-medium text-[#101323]">{title}</h2>
    <div className="mt-2 space-y-2 text-sm leading-6 text-[#4B5563]">{children}</div>
  </section>
);

const LicensesPage = () => (
  <div className="mx-auto max-w-3xl px-7 py-10">
    <h1 className="font-syne text-[22px] font-medium tracking-[-0.66px] text-[#101323]">
      Open-source licenses
    </h1>

    <Section title="Sanrathi Slide Maker">
      <p>
        Sanrathi Slide Maker is based on{" "}
        <a className="underline" href="https://github.com/presenton/presenton" target="_blank" rel="noreferrer">
          Presenton
        </a>
        , licensed under the Apache License 2.0. Sanrathi has modified it; the changed
        files are marked and listed in SANRATHI_CHANGES.md. Presenton is a trademark of
        its owners, who do not endorse Sanrathi.
      </p>
      <p>
        <a className="underline" href="/api/licenses/license" target="_blank">
          Apache License 2.0 (full text)
        </a>
      </p>
    </Section>

    <Section title="Third-party software">
      <p>
        Sanrathi Slide Maker includes third-party packages under their own licenses. Their
        notices are reproduced in the NOTICE file.
      </p>
      <p>
        <a className="underline" href="/api/licenses/notice" target="_blank">
          View NOTICE (third-party attributions)
        </a>
      </p>
    </Section>

    <Section title="AI model">
      <p>
        Slide text is written by Qwen2.5-7B-Instruct (qwen2.5:7b), run locally with Ollama,
        and licensed under the Apache License 2.0.
      </p>
    </Section>

    <Section title="Fonts">
      <p>Poppins and Noto Sans are licensed under the SIL Open Font License 1.1.</p>
    </Section>
  </div>
);

export default LicensesPage;
