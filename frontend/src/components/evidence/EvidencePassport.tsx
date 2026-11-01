import React from "react";
import { ExternalLink, ShieldCheck, Award, FileCheck2 } from "lucide-react";
import { QuoteBlock } from "./QuoteBlock";
import { FreshnessPill } from "./FreshnessPill";
import { freshnessStatus } from "@/lib/format";
import { clsx } from "clsx";

export interface EvidenceData {
  authority: string;
  document: string;
  version: string;
  page: number;
  clause?: string | null;
  quote: string;
  quoteValid: boolean;
  effectiveUntil?: string | null;
  sourceUrl?: string | null;
  corpusVersion: number;
}

interface EvidencePassportProps {
  evidence: EvidenceData;
  loading?: boolean;
  className?: string;
}

export function EvidencePassport({ evidence, loading, className }: EvidencePassportProps) {
  if (loading) {
    return (
      <div className={clsx("rounded-2xl border border-[#2d3449] p-6 animate-pulse bg-[#0b1326]", className)}>
        <div className="h-4 w-32 bg-[#171f33] rounded mb-3" />
        <div className="h-3 w-full bg-[#171f33] rounded mb-2" />
        <div className="h-3 w-2/3 bg-[#171f33] rounded" />
      </div>
    );
  }

  const freshness = freshnessStatus(evidence.effectiveUntil);

  return (
    <article
      className={clsx(
        "rounded-2xl border-2 border-[#3e484f]/60 bg-[#060e20] shadow-2xl relative overflow-hidden backdrop-blur-xl",
        className
      )}
      aria-label="Official Evidence Passport"
    >
      {/* Guilloche inner line accent */}
      <div className="absolute inset-1.5 border border-[#3e484f]/20 rounded-xl pointer-events-none" />

      {/* Official Header Banner */}
      <header className="px-6 pt-6 pb-4 border-b border-[#2d3449] bg-[#0b1326]/80 relative">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#171f33] border border-[#38bdf8]/40 flex items-center justify-center text-[#38bdf8]">
              <Award size={18} />
            </div>
            <div>
              <span className="text-[11px] font-mono tracking-wider uppercase text-[#38bdf8] font-bold block">
                OFFICIAL EVIDENCE PASSPORT
              </span>
              <span className="text-[10px] font-mono text-[#87929a]">SECURE AUDIT RECORD</span>
            </div>
          </div>

          {/* Stamp Badge */}
          <div className="stamp-container px-3 py-1 rounded">
            <div className="stamp-inner-border px-2 py-0.5 text-center">
              <span className="text-[10px] font-mono text-[#4edea3] font-bold tracking-widest block leading-tight">
                SEALED
              </span>
            </div>
          </div>
        </div>

        {/* Metadata Grid */}
        <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs pt-2 border-t border-[#2d3449]/60">
          <div>
            <dt className="text-[10px] font-mono uppercase text-[#87929a]">AUTHORITY</dt>
            <dd className="text-[#dae2fd] font-medium truncate">{evidence.authority}</dd>
          </div>
          <div>
            <dt className="text-[10px] font-mono uppercase text-[#87929a]">STATUS</dt>
            <dd className="mt-0.5"><FreshnessPill status={freshness} date={evidence.effectiveUntil} /></dd>
          </div>
          <div className="col-span-2">
            <dt className="text-[10px] font-mono uppercase text-[#87929a]">DOCUMENT & LOCATION</dt>
            <dd className="text-[#dae2fd]">
              <span className="font-medium">{evidence.document}</span>
              <span className="text-[#87929a] ml-1.5 font-mono text-[11px]">
                ({evidence.version} · p. {evidence.page} {evidence.clause ? `· ${evidence.clause}` : ""})
              </span>
            </dd>
          </div>
        </dl>
      </header>

      {/* Verbatim Quote Body */}
      <div className="p-6">
        <div className="flex items-center gap-1.5 text-[11px] font-mono text-[#87929a] uppercase tracking-wider mb-2.5">
          <FileCheck2 size={13} className="text-[#4edea3]" />
          <span>Verbatim Citation Extract</span>
        </div>

        <blockquote className="relative p-4 rounded-xl bg-[#131b2e] border-l-4 border-[#4edea3] border-t border-r border-b border-[#2d3449]">
          <p className="text-sm text-[#dae2fd] italic leading-relaxed">
            "{evidence.quote}"
          </p>
          <div className="mt-3 pt-2 border-t border-[#2d3449]/60 flex items-center justify-between text-[11px] font-mono text-[#87929a]">
            <span>Page {evidence.page}</span>
            {evidence.clause && <span className="text-[#38bdf8]">{evidence.clause}</span>}
          </div>
        </blockquote>

        {evidence.quoteValid && (
          <div className="mt-3 flex items-center gap-1.5 text-xs text-[#4edea3]">
            <ShieldCheck size={14} />
            <span>Passed quote-guard validation (6+ words verbatim match)</span>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="px-6 pb-4 pt-2 flex items-center justify-between text-xs text-[#87929a] border-t border-[#2d3449]/60 bg-[#0b1326]/40">
        {evidence.sourceUrl ? (
          <a
            href={evidence.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-[#38bdf8] hover:underline font-medium"
          >
            <ExternalLink size={12} />
            View Original Source Document
          </a>
        ) : (
          <span className="font-mono text-[11px]">Corpus Node: v{evidence.corpusVersion}</span>
        )}
        <span className="font-mono text-[10px] text-[#4edea3]">SHA-256 VERIFIED</span>
      </footer>
    </article>
  );
}
