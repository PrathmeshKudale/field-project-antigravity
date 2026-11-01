import React from "react";
import { Check, X, HelpCircle } from "lucide-react";
import { clsx } from "clsx";

interface TraceCondition {
  attr: string;
  op: string;
  value: unknown;
  status: string;
  quote?: string;
}

interface TraceTimelineProps {
  trace: TraceCondition[];
  caveats?: string[];
}

export function TraceTimeline({ trace, caveats }: TraceTimelineProps) {
  return (
    <div className="space-y-3 pt-3">
      <div className="space-y-2">
        {trace.map((item, idx) => (
          <div key={idx} className="flex items-start gap-3 p-2.5 rounded-[var(--r-md)] bg-[var(--surface-2)] text-xs">
            <span
              className={clsx(
                "flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold mt-0.5",
                item.status === "PASS" && "bg-[var(--v-verified-bg)] text-[var(--v-verified-fg)]",
                item.status === "FAIL" && "bg-[var(--v-myth-bg)] text-[var(--v-myth-fg)]",
                item.status === "UNKNOWN" && "bg-[var(--v-context-bg)] text-[var(--v-context-fg)]"
              )}
            >
              {item.status === "PASS" && <Check size={11} />}
              {item.status === "FAIL" && <X size={11} />}
              {item.status === "UNKNOWN" && <HelpCircle size={11} />}
            </span>
            <div className="flex-1">
              <div className="flex items-center justify-between font-mono font-medium text-[var(--ink)]">
                <span>{item.attr} {item.op} {String(item.value)}</span>
                <span className={clsx(
                  "font-bold",
                  item.status === "PASS" && "text-[var(--v-verified-fg)]",
                  item.status === "FAIL" && "text-[var(--v-myth-fg)]",
                  item.status === "UNKNOWN" && "text-[var(--v-context-fg)]"
                )}>
                  {item.status}
                </span>
              </div>
              {item.quote && (
                <p className="mt-1 text-[var(--muted)] font-serif italic">"{item.quote}"</p>
              )}
            </div>
          </div>
        ))}
      </div>
      {caveats && caveats.length > 0 && (
        <div className="p-3 bg-[var(--surface-2)] rounded-[var(--r-md)] border border-[var(--border)] text-xs text-[var(--muted)]">
          <strong>Mandatory caveats:</strong>
          <ul className="list-disc pl-4 mt-1 space-y-0.5">
            {caveats.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
