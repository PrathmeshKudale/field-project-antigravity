import React from "react";
import { Printer, Download, ArrowLeft } from "lucide-react";
import { useTranslation } from "react-i18next";

interface ReportSheetProps {
  question: string;
  verdict: string;
  summary: string;
  explanation: string[];
  evidence: Array<{ authority: string; document: string; page: number; quote: string }>;
  onBack: () => void;
}

export function ReportSheet({ question, verdict, summary, explanation, evidence, onBack }: ReportSheetProps) {
  const { t } = useTranslation();

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-[800px] mx-auto p-6 bg-[var(--surface)] rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e2)] space-y-6">
      <div className="flex items-center justify-between no-print border-b border-[var(--border)] pb-4">
        <button onClick={onBack} className="inline-flex items-center gap-1 text-sm text-[var(--muted)] hover:text-[var(--ink)]">
          <ArrowLeft size={16} /> Back
        </button>
        <button
          onClick={handlePrint}
          className="inline-flex items-center gap-2 px-4 py-2 bg-[var(--primary)] text-white text-sm font-medium rounded-[var(--r-md)]"
        >
          <Printer size={16} /> Print or Save as PDF
        </button>
      </div>

      <div className="border-b border-[var(--border)] pb-4">
        <span className="text-xs uppercase tracking-wider font-bold text-[var(--accent)]">ProofPath Official Family Report</span>
        <h1 className="font-display text-2xl font-bold text-[var(--primary)] mt-1">{t("report.title")}</h1>
        <p className="text-xs text-[var(--muted)] mt-1">Generated: 31 October 2026 · Corpus: v1.0 (Demo)</p>
      </div>

      <section>
        <h3 className="text-xs uppercase font-semibold text-[var(--muted)]">Question Asked</h3>
        <p className="text-base text-[var(--ink)] font-medium mt-1">{question}</p>
      </section>

      <section className="p-4 bg-[var(--surface-2)] rounded-[var(--r-md)] border border-[var(--border)]">
        <h3 className="text-xs uppercase font-semibold text-[var(--muted)]">Verdict</h3>
        <p className="text-lg font-bold text-[var(--primary)] mt-1">{verdict}</p>
        <p className="text-sm text-[var(--ink)] mt-1">{summary}</p>
      </section>

      <section>
        <h3 className="text-xs uppercase font-semibold text-[var(--muted)] mb-2">Verified Explanations</h3>
        <ul className="space-y-1.5 list-disc pl-5 text-sm text-[var(--ink)]">
          {explanation.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3 className="text-xs uppercase font-semibold text-[var(--muted)] mb-2">Official Sources Cited</h3>
        <div className="space-y-2">
          {evidence.map((ev, idx) => (
            <div key={idx} className="p-3 border border-[var(--border)] rounded text-xs">
              <p className="font-medium text-[var(--ink)]">{ev.document} (Page {ev.page}) — {ev.authority}</p>
              <p className="italic text-[var(--muted)] mt-1 font-serif">"{ev.quote}"</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="pt-4 border-t border-[var(--border)] text-xs text-[var(--muted)] text-center">
        {t("footer_disclaimer")}
      </footer>
    </div>
  );
}
