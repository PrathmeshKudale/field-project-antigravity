import React from "react";
import { clsx } from "clsx";

interface NextQuestionChipsProps {
  questions: string[];
  onSelect: (question: string) => void;
}

export function NextQuestionChips({ questions, onSelect }: NextQuestionChipsProps) {
  if (!questions || questions.length === 0) return null;
  return (
    <div className="space-y-2 pt-2">
      <p className="text-sm font-medium text-[var(--muted)]">To be sure, tell us (optional):</p>
      <div className="flex flex-wrap gap-2">
        {questions.map((q, i) => (
          <button
            key={i}
            onClick={() => onSelect(q)}
            className={clsx(
              "px-3.5 py-1.5 rounded-full text-xs font-medium border border-[var(--border)]",
              "bg-[var(--surface)] text-[var(--ink)] hover:border-[var(--accent)] hover:text-[var(--accent)]",
              "transition-all shadow-[var(--e1)]"
            )}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
