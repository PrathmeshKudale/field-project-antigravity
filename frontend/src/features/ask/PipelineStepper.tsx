import React from "react";
import { CheckCircle2, Loader2, Sparkles, Database, ShieldCheck, FileText } from "lucide-react";
import { clsx } from "clsx";

export interface PipelineStage {
  id: string;
  label: string;
  status: "pending" | "active" | "done";
}

interface PipelineStepperProps {
  stages: PipelineStage[];
}

const STAGE_ICONS: Record<string, React.ReactNode> = {
  understand: <Sparkles size={16} />,
  retrieve: <Database size={16} />,
  verify: <ShieldCheck size={16} />,
  explain: <FileText size={16} />,
};

const STAGE_SUBTEXT: Record<string, string> = {
  understand: "NLP semantic parsing & intent extraction",
  retrieve: "Multi-source hybrid RRF retrieval",
  verify: "Verbatim quote validation & 3-valued Kleene engine",
  explain: "Audit trail generation with citation receipts",
};

export function PipelineStepper({ stages }: PipelineStepperProps) {
  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {stages.map((stage, idx) => {
          const isDone = stage.status === "done";
          const isActive = stage.status === "active";
          const isPending = stage.status === "pending";

          return (
            <div
              key={stage.id}
              className={clsx(
                "relative rounded-xl p-3.5 border transition-all duration-300",
                isActive && "bg-[#171f33] border-[#38bdf8] shadow-lg shadow-cyan-500/10 ring-1 ring-[#38bdf8]/40",
                isDone && "bg-[#0f172a] border-[#4edea3]/40",
                isPending && "bg-[#0b1326]/60 border-[#2d3449] opacity-60"
              )}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono tracking-wider uppercase text-[#87929a]">
                  STAGE 0{idx + 1}
                </span>
                {isDone && (
                  <span className="flex items-center gap-1 text-[11px] font-mono text-[#4edea3] font-semibold">
                    <CheckCircle2 size={13} /> DONE
                  </span>
                )}
                {isActive && (
                  <span className="flex items-center gap-1 text-[11px] font-mono text-[#38bdf8] font-semibold">
                    <Loader2 size={13} className="animate-spin" /> ACTIVE
                  </span>
                )}
                {isPending && (
                  <span className="text-[11px] font-mono text-[#87929a]">QUEUED</span>
                )}
              </div>

              <div className="flex items-center gap-2 mb-1">
                <span className={clsx(
                  "p-1.5 rounded-lg",
                  isActive && "bg-[#38bdf8]/20 text-[#38bdf8]",
                  isDone && "bg-[#4edea3]/20 text-[#4edea3]",
                  isPending && "bg-[#171f33] text-[#87929a]"
                )}>
                  {STAGE_ICONS[stage.id] ?? <Sparkles size={16} />}
                </span>
                <h4 className="text-sm font-semibold text-[#dae2fd]">{stage.label}</h4>
              </div>

              <p className="text-xs text-[#87929a] mt-1 line-clamp-2">
                {STAGE_SUBTEXT[stage.id] ?? ""}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
