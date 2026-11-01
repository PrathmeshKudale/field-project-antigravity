import React from "react";
import { CheckCircle2, AlertTriangle, Clock, Ban, type LucideProps } from "lucide-react";
import { clsx } from "clsx";
import { formatDate } from "@/lib/format";

type FreshnessStatus = "current" | "expiring" | "stale" | "superseded";
type LucideIcon = React.ForwardRefExoticComponent<
  Omit<LucideProps, "ref"> & React.RefAttributes<SVGSVGElement>
>;

const CONFIG: Record<FreshnessStatus, { icon: LucideIcon; label: string; classes: string }> = {
  current: { icon: CheckCircle2, label: "Current", classes: "text-[var(--v-verified-fg)] bg-[var(--v-verified-bg)]" },
  expiring: { icon: Clock, label: "Expiring soon", classes: "text-[var(--v-context-fg)] bg-[var(--v-context-bg)]" },
  stale: { icon: AlertTriangle, label: "Stale", classes: "text-[var(--v-insuff-fg)] bg-[var(--v-insuff-bg)]" },
  superseded: { icon: Ban, label: "Superseded", classes: "text-[var(--v-myth-fg)] bg-[var(--v-myth-bg)]" },
};

interface FreshnessPillProps {
  status: FreshnessStatus;
  date?: string | null;
}

export function FreshnessPill({ status, date }: FreshnessPillProps) {
  const config = CONFIG[status] ?? CONFIG.current;
  const Icon = config.icon;
  return (
    <span className={clsx("inline-flex items-center gap-1.5 text-xs px-2.5 py-0.5 rounded-full font-medium", config.classes)}>
      <Icon size={12} aria-hidden />
      {config.label}
      {date && <span className="opacity-80">· to {formatDate(date)}</span>}
    </span>
  );
}
