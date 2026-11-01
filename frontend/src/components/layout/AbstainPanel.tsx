import React from "react";
import { SearchX, HelpCircle, ArrowRight } from "lucide-react";
import { useTranslation } from "react-i18next";

interface AbstainPanelProps {
  missing?: string;
  authorityHint?: string;
  suggestions?: string[];
  onSuggestionClick?: (query: string) => void;
}

export function AbstainPanel({ missing, authorityHint = "State Board of Technical Education Helpline", suggestions, onSuggestionClick }: AbstainPanelProps) {
  const { t } = useTranslation();
  const defaultSuggestions = [
    "ITI Electrician ke baad diploma kaise milega?",
    "Direct Second Year diploma eligibility rules kya hain?",
    "Diploma in Engineering ke baad B.Tech lateral entry process",
  ];
  const items = suggestions && suggestions.length > 0 ? suggestions : defaultSuggestions;

  return (
    <div className="rounded-[var(--r-lg)] bg-[var(--v-insuff-bg)] border border-[var(--border)] p-6 text-center shadow-[var(--e1)]">
      <SearchX size={44} className="mx-auto mb-3 text-[var(--v-insuff-fg)]" aria-hidden />
      <h3 className="font-display text-xl font-semibold text-[var(--primary)] mb-2">
        {t("abstain.title")}
      </h3>
      <p className="text-[var(--muted)] text-sm max-w-md mx-auto mb-5">
        {missing ?? t("abstain.body")}
      </p>

      <div className="inline-flex items-center gap-2 text-sm text-[var(--ink)] bg-[var(--surface)] border border-[var(--border)] rounded-[var(--r-md)] px-4 py-2.5 mb-6 shadow-sm">
        <HelpCircle size={16} className="text-[var(--accent)]" aria-hidden />
        <span>{t("abstain.who_to_ask")}: <strong>{authorityHint}</strong></span>
      </div>

      <div className="text-left max-w-md mx-auto bg-[var(--surface)] p-4 rounded-[var(--r-md)] border border-[var(--border)]">
        <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)] mb-2">Try asking instead:</p>
        <ul className="space-y-1.5">
          {items.map((s, i) => (
            <li
              key={i}
              onClick={() => onSuggestionClick?.(s)}
              className="text-sm text-[var(--accent)] hover:underline cursor-pointer flex items-center gap-1.5"
            >
              <ArrowRight size={13} className="shrink-0" />
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
