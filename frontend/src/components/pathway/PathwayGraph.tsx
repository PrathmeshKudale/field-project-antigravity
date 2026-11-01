import React from "react";
import { clsx } from "clsx";
import { CheckCircle2, XCircle, HelpCircle } from "lucide-react";

interface PathwayRoute {
  route: string;
  title: string;
  status: string;
  eligibility: string;
}

interface PathwayGraphProps {
  routes: PathwayRoute[];
  selectedRoute: string | null;
  onSelect: (routeKey: string) => void;
}

export function PathwayGraph({ routes, selectedRoute, onSelect }: PathwayGraphProps) {
  return (
    <div className="p-4 bg-[var(--surface-2)] rounded-[var(--r-lg)] border border-[var(--border)]">
      <div className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)] mb-3">
        Interactive Pathway Graph
      </div>
      <div className="space-y-3">
        {routes.map((r) => {
          const isSelected = selectedRoute === r.route;
          return (
            <button
              key={r.route}
              onClick={() => onSelect(r.route)}
              className={clsx(
                "w-full text-left p-4 rounded-[var(--r-md)] border transition-all flex items-center justify-between",
                isSelected
                  ? "bg-[var(--surface)] border-[var(--accent)] ring-2 ring-[var(--accent)] shadow-[var(--e1)]"
                  : "bg-[var(--surface)] border-[var(--border)] hover:border-[var(--muted)]"
              )}
            >
              <div>
                <h4 className="font-semibold text-sm text-[var(--ink)]">{r.title}</h4>
                <p className="text-xs text-[var(--muted)] font-mono">{r.route}</p>
              </div>
              <span className={clsx(
                "inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full font-medium shrink-0",
                r.status === "PASS" && "bg-[var(--v-verified-bg)] text-[var(--v-verified-fg)]",
                r.status === "FAIL" && "bg-[var(--v-myth-bg)] text-[var(--v-myth-fg)]",
                r.status === "UNKNOWN" && "bg-[var(--v-context-bg)] text-[var(--v-context-fg)]"
              )}>
                {r.status === "PASS" && <CheckCircle2 size={12} />}
                {r.status === "FAIL" && <XCircle size={12} />}
                {r.status === "UNKNOWN" && <HelpCircle size={12} />}
                {r.status}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
