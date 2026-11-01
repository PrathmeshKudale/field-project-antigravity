import React, { useState, useRef } from "react";
import { Search, Sparkles, Command } from "lucide-react";
import { useTranslation } from "react-i18next";
import { clsx } from "clsx";

const MAX_CHARS = 600;

interface AskComposerProps {
  onSubmit: (question: string) => void;
  disabled?: boolean;
  loading?: boolean;
}

export function AskComposer({ onSubmit, disabled, loading }: AskComposerProps) {
  const { t } = useTranslation();
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const charCount = value.length;
  const overLimit = charCount > MAX_CHARS;

  const exampleChips = [
    { label: "ITI to B.Tech Direct Myth?", icon: "⚡" },
    { label: "ITI Electrician to Diploma 2nd Year?", icon: "🔌" },
    { label: "Lateral Entry to B.Tech with 48%?", icon: "🎓" },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim() || overLimit || disabled || loading) return;
    onSubmit(value.trim());
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      {/* Search Bar Container with Glowing Azure Accent */}
      <div className="relative rounded-2xl p-1 bg-surface-container-high/90 border border-primary-container/40 backdrop-blur-xl ambient-cyan-glow">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 bg-[#060e20]/90 rounded-xl p-2.5 border border-[#3e484f]/40">
          <div className="flex items-center pl-3 pr-1 text-[#38bdf8]">
            <Search size={22} />
          </div>

          <label htmlFor="ask-input" className="sr-only">Ask a question</label>
          <textarea
            ref={textareaRef}
            id="ask-input"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about vocational routes (e.g., Can 2-yr ITI enter Diploma 2nd year?)..."
            disabled={disabled || loading}
            rows={2}
            className={clsx(
              "w-full bg-transparent border-0 text-[#dae2fd] placeholder:text-[#87929a] text-base focus:ring-0 focus:outline-none resize-none py-1.5 px-2",
              overLimit && "text-red-400",
              (disabled || loading) && "opacity-50 cursor-not-allowed"
            )}
            maxLength={MAX_CHARS}
          />

          <div className="hidden lg:flex items-center pr-2">
            <kbd className="px-2 py-1 rounded bg-[#171f33] border border-[#3e484f] text-[11px] font-mono text-[#87929a] flex items-center gap-0.5">
              <Command size={11} /> Enter
            </kbd>
          </div>

          <button
            type="submit"
            disabled={!value.trim() || overLimit || disabled || loading}
            className={clsx(
              "flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium text-sm transition-all duration-200 shrink-0",
              "bg-gradient-to-r from-[#0284c7] to-[#0369a1] text-white border border-[#38bdf8]/60 shadow-lg shadow-cyan-500/20",
              "hover:brightness-110 active:scale-[0.98]",
              (!value.trim() || overLimit || disabled || loading) && "opacity-50 cursor-not-allowed filter-none"
            )}
          >
            {loading ? (
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Sparkles size={16} className="text-cyan-200" />
            )}
            <span>{loading ? "Verifying..." : "Verify Evidence"}</span>
          </button>
        </div>

        {/* Telemetry bar beneath input */}
        <div className="flex items-center justify-between px-3 pt-2 pb-1 text-[11px] font-mono text-[#87929a]">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#4edea3] animate-pulse"></span>
            Deterministic Rule Engine Active
          </span>
          <span>{charCount}/{MAX_CHARS}</span>
        </div>
      </div>

      {/* Quick Question Chips */}
      <div className="flex flex-wrap items-center gap-2 pt-1">
        <span className="text-xs font-mono uppercase tracking-wider text-[#87929a]">
          Verified Prompts:
        </span>
        {exampleChips.map((chip, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => {
              setValue(chip.label);
              textareaRef.current?.focus();
            }}
            className="px-3 py-1.5 rounded-lg bg-[#171f33] hover:bg-[#222a3d] border border-[#3e484f]/60 text-xs text-[#dae2fd] hover:text-[#8ed5ff] transition-all flex items-center gap-1.5 hover:border-[#38bdf8]/50"
          >
            <span>{chip.icon}</span>
            <span>{chip.label}</span>
          </button>
        ))}
      </div>
    </form>
  );
}
