import React from "react";
import {
  ShieldCheck,
  OctagonX,
  CircleDotDashed,
  GitBranch,
  SearchX,
  AlertTriangle,
  type LucideProps,
} from "lucide-react";
import { clsx } from "clsx";
import type { VerdictType } from "./VerdictBadge";

type LucideIcon = React.ForwardRefExoticComponent<
  Omit<LucideProps, "ref"> & React.RefAttributes<SVGSVGElement>
>;

const HERO_CONFIG: Record<VerdictType, {
  icon: LucideIcon;
  headline: string;
  classes: string;
  bgClasses: string;
}> = {
  VERIFIED_FACT: {
    icon: ShieldCheck,
    headline: "Supported by official sources",
    classes: "text-[var(--v-verified-fg)]",
    bgClasses: "bg-[var(--v-verified-bg)]",
  },
  MYTH_FALSE: {
    icon: OctagonX,
    headline: "Not supported: sources say otherwise",
    classes: "text-[var(--v-myth-fg)]",
    bgClasses: "bg-[var(--v-myth-bg)]",
  },
  PARTIALLY_TRUE: {
    icon: CircleDotDashed,
    headline: "Partly true: details matter",
    classes: "text-[var(--v-partial-fg)]",
    bgClasses: "bg-[var(--v-partial-bg)]",
  },
  CONTEXT_DEPENDENT: {
    icon: GitBranch,
    headline: "Depends on your situation",
    classes: "text-[var(--v-context-fg)]",
    bgClasses: "bg-[var(--v-context-bg)]",
  },
  INSUFFICIENT_EVIDENCE: {
    icon: SearchX,
    headline: "We could not verify this",
    classes: "text-[var(--v-insuff-fg)]",
    bgClasses: "bg-[var(--v-insuff-bg)]",
  },
};

interface VerdictHeroProps {
  verdict: VerdictType;
  summary: string;
  verifiedCount: number;
  totalCount: number;
  reviewFlag?: boolean;
  loading?: boolean;
}

export function VerdictHero({ verdict, summary, verifiedCount, totalCount, reviewFlag, loading }: VerdictHeroProps) {
  if (loading) {
    return (
      <div className="rounded-[var(--r-lg)] p-6 bg-[var(--surface-2)] animate-pulse">
        <div className="h-8 w-48 bg-[var(--border)] rounded mb-3" />
        <div className="h-5 w-full bg-[var(--border)] rounded mb-2" />
        <div className="h-4 w-32 bg-[var(--border)] rounded" />
      </div>
    );
  }

  const config = HERO_CONFIG[verdict] ?? HERO_CONFIG.CONTEXT_DEPENDENT;
  const Icon = config.icon;

  return (
    <div className={clsx("rounded-[var(--r-lg)] p-6 border border-[var(--border)] shadow-[var(--e1)]", config.bgClasses)}>
      <div className={clsx("flex items-center gap-3 mb-3", config.classes)}>
        <Icon size={32} aria-hidden />
        <h2 className="font-display text-[1.75rem] leading-[1.2] font-semibold">{config.headline}</h2>
      </div>
      <p className="text-[var(--ink)] text-base leading-relaxed mb-4">{summary}</p>
      {totalCount > 0 && (
        <div className="flex items-center gap-3" aria-label={`Evidence strength: ${verifiedCount} of ${totalCount} statements verified`}>
          <span className="text-sm text-[var(--muted)]">Evidence strength:</span>
          <div className="flex gap-1 flex-1 max-w-xs" aria-hidden>
            {Array.from({ length: totalCount }).map((_, i) => (
              <div
                key={i}
                className={clsx(
                  "h-2.5 flex-1 rounded-full transition-colors",
                  i < verifiedCount ? "bg-[var(--accent)]" : "bg-[var(--border)]"
                )}
              />
            ))}
          </div>
          <span className="text-sm font-medium text-[var(--muted)]">{verifiedCount} of {totalCount} verified</span>
        </div>
      )}
      {reviewFlag && (
        <div className="mt-3 flex items-center gap-2 text-sm text-[var(--muted)]">
          <AlertTriangle size={14} aria-hidden />
          <span>Queued for expert review</span>
        </div>
      )}
    </div>
  );
}
