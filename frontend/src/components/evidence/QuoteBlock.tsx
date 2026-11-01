import React, { useState } from "react";
import { Copy, CheckCheck } from "lucide-react";
import { clsx } from "clsx";

interface QuoteBlockProps {
  text: string;
  page?: number;
  clause?: string | null;
}

export function QuoteBlock({ text, page, clause }: QuoteBlockProps) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isLong = text.length > 200;
  const displayText = !expanded && isLong ? text.slice(0, 200) + "…" : text;

  return (
    <div className="relative group bg-[var(--surface-2)] rounded-[var(--r-md)] p-3 border border-[var(--border)]">
      <blockquote className="border-l-4 border-[var(--accent)] pl-3 py-1 pr-8 font-serif italic text-[var(--ink)] leading-relaxed text-sm">
        <mark className="bg-[var(--mark)] rounded px-1 not-italic font-sans">{displayText}</mark>
        {isLong && !expanded && (
          <button
            onClick={() => setExpanded(true)}
            className="ml-2 text-[var(--accent)] underline text-xs not-italic"
          >
            Show full quote
          </button>
        )}
      </blockquote>
      <div className="mt-2 flex items-center justify-between text-xs text-[var(--muted)]">
        <span>
          {page && `Page ${page}`}
          {clause && ` · ${clause}`}
        </span>
        <button
          onClick={handleCopy}
          aria-label="Copy quote"
          className="inline-flex items-center gap-1 text-[var(--muted)] hover:text-[var(--accent)]"
        >
          {copied ? <CheckCheck size={13} /> : <Copy size={13} />}
          <span>{copied ? "Copied" : "Copy"}</span>
        </button>
      </div>
    </div>
  );
}
