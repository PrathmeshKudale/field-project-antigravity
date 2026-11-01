import React, { useState } from "react";
import { Check, X, ShieldAlert, Sparkles, BookOpen } from "lucide-react";

interface RuleCandidate {
  rule_id: string;
  route: string;
  title: string;
  status: string;
  source_page: number;
  maker: string;
  schema_valid: boolean;
  quotes_valid: boolean;
  conditions: any;
}

export function StudioPage() {
  const [candidates, setCandidates] = useState<RuleCandidate[]>([
    {
      rule_id: "DEMO-DSE-001",
      route: "ITI_TO_DIPLOMA_DSE",
      title: "Direct Second Year Diploma (DSE) Admission for ITI Holders",
      status: "in_review",
      source_page: 3,
      maker: "kulkarni@polytechnic.example",
      schema_valid: true,
      quotes_valid: true,
      conditions: {
        all: [
          { attr: "ssc.passed", op: "eq", value: true, quote: "A candidate who has passed the Class X examination" },
          { attr: "qualification.type", op: "in", value: ["ITI"], quote: "and holds a Two-Year Craft Certificate" },
          { attr: "craft_certificate.mapped_trade", op: "eq", value: true, quote: "in a Mapped Trade" },
          { attr: "marks.percent", op: "gte", value: 50.0, quote: "shall be eligible for Direct Second Year admission" },
        ],
      },
    },
    {
      rule_id: "DEMO-NOTE-01",
      route: "ITI_TO_DEGREE_DIRECT",
      title: "Direct Degree Entry Prohibited for ITI Standalone",
      status: "approved",
      source_page: 4,
      maker: "admin@proofpath.example",
      schema_valid: true,
      quotes_valid: true,
      conditions: {
        all: [
          { attr: "qualification.type", op: "ne", value: "ITI", quote: "Holders of National Trade Certificates (ITI) without a recognised Polytechnic Diploma shall not be admitted directly" },
        ],
      },
    },
  ]);

  const [selectedIdx, setSelectedIdx] = useState(0);
  const selected = candidates[selectedIdx];

  const handleApprove = (id: string) => {
    setCandidates((prev) =>
      prev.map((c) => (c.rule_id === id ? { ...c, status: "approved" } : c))
    );
  };

  const handleReject = (id: string) => {
    setCandidates((prev) =>
      prev.map((c) => (c.rule_id === id ? { ...c, status: "rejected" } : c))
    );
  };

  return (
    <div className="max-w-[1200px] mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="font-display text-[2rem] font-bold text-[var(--primary)]">Rule Studio</h1>
          <p className="text-sm text-[var(--muted)]">
            Maker-Checker Governance: Review and publish versioned eligibility rules with verbatim citations.
          </p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-[var(--surface)] border border-[var(--border)] rounded text-xs">
          <ShieldAlert size={14} className="text-[var(--accent)]" />
          <span>Maker != Checker Enforced</span>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-6 items-start">
        {/* Left Queue */}
        <div className="lg:col-span-4 bg-[var(--surface)] p-4 rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)]">
          <h3 className="text-xs uppercase font-bold text-[var(--muted)] tracking-wider mb-3">
            Review Queue ({candidates.length})
          </h3>
          <div className="space-y-2">
            {candidates.map((c, i) => (
              <div
                key={c.rule_id}
                onClick={() => setSelectedIdx(i)}
                className={`p-3 rounded-[var(--r-md)] border cursor-pointer transition-all ${
                  selectedIdx === i
                    ? "bg-[var(--surface-2)] border-[var(--accent)]"
                    : "bg-[var(--surface)] border-[var(--border)] hover:border-[var(--muted)]"
                }`}
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-mono font-bold text-[var(--ink)]">{c.rule_id}</span>
                  <span className="capitalize px-2 py-0.5 rounded text-[10px] font-semibold bg-[var(--surface-2)]">
                    {c.status}
                  </span>
                </div>
                <p className="text-xs text-[var(--muted)] mt-1 truncate">{c.title}</p>
                <div className="mt-2 flex items-center justify-between text-[11px] text-[var(--muted)]">
                  <span>Page {c.source_page}</span>
                  <span className="text-[var(--v-verified-fg)]">Quotes verified ✓</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Center Source Text */}
        <div className="lg:col-span-4 bg-[var(--surface)] p-5 rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)]">
          <div className="flex items-center gap-1.5 text-xs uppercase font-bold text-[var(--muted)] tracking-wider mb-3">
            <BookOpen size={14} /> Official Source Document
          </div>
          <div className="p-4 bg-[var(--surface-2)] rounded border border-[var(--border)] font-serif text-xs leading-relaxed text-[var(--ink)]">
            <p className="font-bold font-sans text-xs mb-2">Admission Handbook 2026-27 (Page {selected?.source_page})</p>
            <p>
              <mark className="bg-[var(--mark)] px-1 rounded">
                "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate in a Mapped Trade shall be eligible for Direct Second Year admission to a Diploma in a Mapped Branch of Engineering and Technology."
              </mark>
            </p>
            <p className="mt-3 text-[var(--muted)] font-sans text-[11px]">
              Clause 3.1 & 3.4 · Domicile and seat rosters apply.
            </p>
          </div>
        </div>

        {/* Right Rule Inspector */}
        <div className="lg:col-span-4 bg-[var(--surface)] p-5 rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)] space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs uppercase font-bold text-[var(--muted)] tracking-wider">Rule Inspector</h3>
            <span className="text-xs font-mono font-bold text-[var(--accent)]">{selected?.rule_id}</span>
          </div>

          <div className="text-xs space-y-1">
            <p><strong>Route:</strong> <code>{selected?.route}</code></p>
            <p><strong>Maker:</strong> {selected?.maker}</p>
            <p><strong>Schema:</strong> <span className="text-[var(--v-verified-fg)]">Valid JSON DSL ✓</span></p>
          </div>

          <div className="p-3 bg-[var(--surface-2)] rounded text-xs space-y-2 border border-[var(--border)] font-mono">
            {selected?.conditions.all?.map((cond: any, idx: number) => (
              <div key={idx} className="p-1.5 bg-[var(--surface)] rounded border border-[var(--border)]">
                <span className="font-bold">{cond.attr}</span> {cond.op} {String(cond.value)}
                <p className="text-[10px] text-[var(--muted)] font-serif italic mt-0.5">"{cond.quote}"</p>
              </div>
            ))}
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={() => handleApprove(selected.rule_id)}
              className="flex-1 py-2 bg-[var(--accent)] text-white text-xs font-semibold rounded hover:opacity-90 flex items-center justify-center gap-1"
            >
              <Check size={14} /> Approve (Checker)
            </button>
            <button
              onClick={() => handleReject(selected.rule_id)}
              className="py-2 px-3 border border-[var(--v-myth-fg)] text-[var(--v-myth-fg)] text-xs font-semibold rounded hover:bg-[var(--v-myth-bg)] flex items-center justify-center"
            >
              <X size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
