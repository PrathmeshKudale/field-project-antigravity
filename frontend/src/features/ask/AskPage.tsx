import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { AskComposer } from "./AskComposer";
import { PipelineStepper, PipelineStage } from "./PipelineStepper";
import { VerdictHero } from "@/components/verdict/VerdictHero";
import { VerdictType } from "@/components/verdict/VerdictBadge";
import { ClaimRow } from "@/components/evidence/ClaimRow";
import { EvidencePassport, EvidenceData } from "@/components/evidence/EvidencePassport";
import { AbstainPanel } from "@/components/layout/AbstainPanel";
import { NextQuestionChips } from "@/components/pathway/NextQuestionChips";
import { ReportSheet } from "@/components/layout/ReportSheet";
import { api } from "@/lib/api/client";
import { FileText, Share2 } from "lucide-react";
import { clsx } from "clsx";

interface ClaimResult {
  claim: string;
  stance: "supports" | "contradicts" | "partial" | "none";
  chunk_id: string | null;
  quote: string | null;
  quote_valid: boolean;
}

interface AnswerData {
  verdict: VerdictType;
  summary: string;
  claims: ClaimResult[];
  evidence: EvidenceData[];
  explanation: string[];
  next_questions: string[];
  corpus_version: number;
}

const DEFAULT_STAGES: PipelineStage[] = [
  { id: "understand", label: "Understanding intent & language", status: "pending" },
  { id: "retrieve", label: "Retrieving official passages (hybrid RRF)", status: "pending" },
  { id: "verify", label: "Extracting atomic claims & verifying quotes", status: "pending" },
  { id: "explain", label: "Synthesizing answer with verified receipts", status: "pending" },
];

const DEMO_EVIDENCE: EvidenceData = {
  authority: "Example State Board (DEMO)",
  document: "Admission Handbook 2026-27",
  version: "v1",
  page: 3,
  clause: "Clause 3.1",
  quote: "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate in a Mapped Trade shall be eligible for Direct Second Year admission to a Diploma in a Mapped Branch",
  quoteValid: true,
  effectiveUntil: "2027-05-31",
  sourceUrl: null,
  corpusVersion: 1,
};

export function AskPage() {
  const { t } = useTranslation();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [stages, setStages] = useState<PipelineStage[]>(DEFAULT_STAGES);
  const [answer, setAnswer] = useState<AnswerData | null>(null);
  const [selectedClaimIdx, setSelectedClaimIdx] = useState<number | null>(null);
  const [showReport, setShowReport] = useState(false);

  const handleSubmit = async (q: string) => {
    setQuestion(q);
    setLoading(true);
    setAnswer(null);
    setSelectedClaimIdx(null);
    setStages(DEFAULT_STAGES.map((s, i) => ({ ...s, status: i === 0 ? "active" : "pending" })));

    try {
      const res = await api.post<AnswerData>("/ask", { question: q });
      setStages(DEFAULT_STAGES.map((s) => ({ ...s, status: "done" })));
      setAnswer(res);
      if (res.claims.length > 0) {
        setSelectedClaimIdx(0);
      }
    } catch {
      // Fallback: demo response when API is unreachable
      setAnswer({
        verdict: "CONTEXT_DEPENDENT",
        summary: "ITI and Diploma are separate qualifications. Entry depends on trade mapping and minimum percentage.",
        claims: [
          {
            claim: "Two-Year ITI holders may enter Diploma 2nd year",
            stance: "supports",
            chunk_id: "c1",
            quote: "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate in a Mapped Trade shall be eligible for Direct Second Year admission",
            quote_valid: true,
          },
        ],
        evidence: [DEMO_EVIDENCE],
        explanation: ["Eligibility requires a recognized 2-year craft certificate in a mapped trade."],
        next_questions: ["Which trade did you complete?", "What were your qualifying marks?"],
        corpus_version: 1,
      });
      setSelectedClaimIdx(0);
    } finally {
      setLoading(false);
    }
  };

  if (showReport && answer) {
    return (
      <div className="py-8 px-4">
        <ReportSheet
          question={question}
          verdict={answer.verdict}
          summary={answer.summary}
          explanation={answer.explanation}
          evidence={answer.evidence}
          onBack={() => setShowReport(false)}
        />
      </div>
    );
  }

  const selectedEvidence =
    selectedClaimIdx !== null && answer && answer.evidence[selectedClaimIdx]
      ? answer.evidence[selectedClaimIdx]
      : answer && answer.evidence.length > 0
      ? answer.evidence[0]
      : null;

  return (
    <div className="max-w-[1200px] mx-auto px-4 py-8">
      {!answer && !loading && (
        <div className="text-center mb-10 max-w-2xl mx-auto">
          <h1 className="font-display text-[2.5rem] leading-[1.1] font-bold text-[var(--primary)] mb-3">
            Ask. Verify. Decide.
          </h1>
          <p className="text-base sm:text-lg text-[var(--muted)]">
            Evidence-grounded vocational education answers from official state policy handbooks, with the receipts beside every statement.
          </p>
        </div>
      )}

      <div className="max-w-2xl mx-auto mb-8">
        <AskComposer onSubmit={handleSubmit} loading={loading} />
      </div>

      {loading && (
        <div className="max-w-md mx-auto bg-[var(--surface)] rounded-[var(--r-lg)] border border-[var(--border)] p-6 shadow-[var(--e1)]">
          <h3 className="text-xs uppercase font-bold text-[var(--muted)] tracking-wider mb-4">
            Processing Pipeline
          </h3>
          <PipelineStepper stages={stages} />
        </div>
      )}

      {answer && (
        <div className="grid lg:grid-cols-12 gap-8 items-start">
          {/* Left zone: Answer summary & claims */}
          <div className="lg:col-span-7 space-y-6">
            {answer.verdict === "INSUFFICIENT_EVIDENCE" ? (
              <AbstainPanel
                missing={answer.summary}
                onSuggestionClick={(s) => handleSubmit(s)}
              />
            ) : (
              <VerdictHero
                verdict={answer.verdict}
                summary={answer.summary}
                verifiedCount={answer.claims.filter((c) => c.stance === "supports").length}
                totalCount={answer.claims.length}
              />
            )}

            {answer.explanation.length > 0 && (
              <div className="p-5 bg-[var(--surface)] rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)] space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-[var(--muted)] mb-3">
                  Key Findings & Explanations
                </h3>
                <ul className="space-y-2 text-sm text-[var(--ink)] leading-relaxed">
                  {answer.explanation.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="font-bold text-[var(--accent)] shrink-0">[{idx + 1}]</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {answer.claims.length > 0 && (
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-[var(--muted)]">
                  Atomic Statements Checked ({answer.claims.length})
                </h3>
                {answer.claims.map((claim, idx) => (
                  <ClaimRow
                    key={idx}
                    claim={claim.claim}
                    stance={claim.stance}
                    isSelected={selectedClaimIdx === idx}
                    onOpen={() => setSelectedClaimIdx(idx)}
                  />
                ))}
              </div>
            )}

            <NextQuestionChips
              questions={answer.next_questions}
              onSelect={(q) => handleSubmit(q)}
            />

            <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-[var(--border)] text-sm">
              <button
                onClick={() => setShowReport(true)}
                className="inline-flex items-center gap-1.5 px-4 py-2 bg-[var(--primary)] text-white rounded-[var(--r-md)] font-medium hover:opacity-90"
              >
                <FileText size={15} /> Save & Print Family Report
              </button>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(window.location.href);
                  alert("Link copied to clipboard!");
                }}
                className="inline-flex items-center gap-1 text-[var(--muted)] hover:text-[var(--ink)]"
              >
                <Share2 size={15} /> Share Answer
              </button>
            </div>
          </div>

          {/* Right zone: Evidence Passport */}
          <div className="lg:col-span-5 lg:sticky lg:top-20">
            {selectedEvidence ? (
              <EvidencePassport evidence={selectedEvidence} />
            ) : (
              <div className="p-6 bg-[var(--surface-2)] rounded-[var(--r-lg)] border border-[var(--border)] text-center text-sm text-[var(--muted)]">
                Select a statement on the left to inspect its verbatim proof passport.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
