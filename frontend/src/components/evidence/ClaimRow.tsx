import React from "react";
import { ChevronRight } from "lucide-react";
import { clsx } from "clsx";

type ClaimStance = "supports" | "contradicts" | "partial" | "none";

const STANCE_CONFIG: Record<ClaimStance, { label: string; classes: string }> = {
  supports: { label: "Supported", classes: "text-[var(--v-verified-fg)] bg-[var(--v-verified-bg)]" },
  contradicts: { label: "Not supported", classes: "text-[var(--v-myth-fg)] bg-[var(--v-myth-bg)]" },
  partial: { label: "Partly true", classes: "text-[var(--v-partial-fg)] bg-[var(--v-partial-bg)]" },
  none: { label: "Need info", classes: "text-[var(--v-context-fg)] bg-[var(--v-context-bg)]" },
};

interface ClaimRowProps {
  claim: string;
  stance: ClaimStance;
  isSelected?: boolean;
  onOpen?: () => void;
}

export function ClaimRow({ claim, stance, isSelected, onOpen }: ClaimRowProps) {
  const config = STANCE_CONFIG[stance] ?? STANCE_CONFIG.none;
  return (
    <div
      onClick={onOpen}
      className={clsx(
        "flex items-center justify-between py-3 px-4 rounded-[var(--r-md)] border cursor-pointer transition-all",
        isSelected
          ? "bg-[var(--surface-2)] border-[var(--accent)] shadow-[var(--e1)] ring-1 ring-[var(--accent)]"
          : "bg-[var(--surface)] border-[var(--border)] hover:border-[var(--muted)]"
      )}
    >
      <div className="flex items-center gap-3 min-w-0 pr-2">
        <span className={clsx("text-xs px-2.5 py-0.5 rounded-full font-medium whitespace-nowrap shrink-0", config.classes)}>
          {config.label}
        </span>
        <span className="text-sm text-[var(--ink)] truncate">{claim}</span>
      </div>
      <button
        type="button"
        className="flex items-center gap-1 text-xs text-[var(--accent)] hover:underline whitespace-nowrap shrink-0 font-medium"
      >
        Proof <ChevronRight size={13} aria-hidden />
      </button>
    </div>
  );
}
