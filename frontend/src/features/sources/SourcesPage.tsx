import React from "react";
import { CheckCircle2, FileText, ExternalLink } from "lucide-react";

export function SourcesPage() {
  const sources = [
    {
      title: "Admission Handbook for Diploma & Post-Diploma Programmes (2026-27)",
      authority: "Example State Board of Technical Education (DEMO)",
      version: "v1.0",
      status: "current",
      effective: "01 Jun 2026 to 31 May 2027",
      pages: 8,
      clauses: 14,
    },
  ];

  return (
    <div className="max-w-[1200px] mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="font-display text-[2rem] font-bold text-[var(--primary)]">Sources & Source Health</h1>
        <p className="text-sm text-[var(--muted)] mt-1">
          Catalog of ingested regulator documents powering claim verification and rule authoring.
        </p>
      </div>

      <div className="space-y-4">
        {sources.map((s, idx) => (
          <div key={idx} className="p-6 bg-[var(--surface)] rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)] flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-[var(--v-verified-bg)] text-[var(--v-verified-fg)] font-semibold uppercase tracking-wider flex items-center gap-1">
                  <CheckCircle2 size={12} /> {s.status}
                </span>
                <span className="text-xs text-[var(--muted)]">{s.version}</span>
              </div>
              <h3 className="font-bold text-base text-[var(--ink)]">{s.title}</h3>
              <p className="text-xs text-[var(--muted)]">{s.authority} · Effective: {s.effective}</p>
            </div>
            <div className="flex items-center gap-4 text-xs font-mono text-[var(--muted)]">
              <span>{s.pages} Pages</span>
              <span>·</span>
              <span>{s.clauses} Chunks</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
