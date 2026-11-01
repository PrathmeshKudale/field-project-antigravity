import React from "react";
import {
  ShieldCheck,
  OctagonX,
  CircleDotDashed,
  GitBranch,
  SearchX,
  type LucideProps,
} from "lucide-react";
import { clsx } from "clsx";

export type VerdictType =
  | "VERIFIED_FACT"
  | "MYTH_FALSE"
  | "PARTIALLY_TRUE"
  | "CONTEXT_DEPENDENT"
  | "INSUFFICIENT_EVIDENCE";

type LucideIcon = React.ForwardRefExoticComponent<
  Omit<LucideProps, "ref"> & React.RefAttributes<SVGSVGElement>
>;

const VERDICT_CONFIG: Record<VerdictType, { icon: LucideIcon; label: string; classes: string }> = {
  VERIFIED_FACT: { icon: ShieldCheck, label: "Supported", classes: "text-[var(--v-verified-fg)] bg-[var(--v-verified-bg)]" },
  MYTH_FALSE: { icon: OctagonX, label: "Not supported", classes: "text-[var(--v-myth-fg)] bg-[var(--v-myth-bg)]" },
  PARTIALLY_TRUE: { icon: CircleDotDashed, label: "Partly true", classes: "text-[var(--v-partial-fg)] bg-[var(--v-partial-bg)]" },
  CONTEXT_DEPENDENT: { icon: GitBranch, label: "Depends on situation", classes: "text-[var(--v-context-fg)] bg-[var(--v-context-bg)]" },
  INSUFFICIENT_EVIDENCE: { icon: SearchX, label: "Not verified", classes: "text-[var(--v-insuff-fg)] bg-[var(--v-insuff-bg)]" },
};

interface VerdictBadgeProps {
  verdict: VerdictType;
  size?: "sm" | "md";
  className?: string;
}

export function VerdictBadge({ verdict, size = "md", className }: VerdictBadgeProps) {
  const config = VERDICT_CONFIG[verdict] ?? VERDICT_CONFIG.CONTEXT_DEPENDENT;
  const Icon = config.icon;
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 font-medium rounded-full",
        size === "sm" ? "text-xs px-2.5 py-0.5" : "text-sm px-3.5 py-1",
        config.classes,
        className
      )}
      aria-label={`Verdict: ${config.label}`}
    >
      <Icon size={size === "sm" ? 12 : 15} aria-hidden />
      {config.label}
    </span>
  );
}
