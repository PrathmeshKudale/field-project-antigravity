import React, { ReactNode } from "react";

interface DialogProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Dialog({ open, onClose, title, children }: DialogProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" role="dialog" aria-modal aria-labelledby="dialog-title">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-[var(--surface)] rounded-[var(--r-lg)] shadow-[var(--e2)] p-6 max-w-md w-full mx-4 z-10 border border-[var(--border)]">
        <h2 id="dialog-title" className="font-semibold text-[var(--primary)] mb-4">{title}</h2>
        {children}
        <button onClick={onClose} className="absolute top-4 right-4 text-[var(--muted)] hover:text-[var(--ink)]" aria-label="Close">✕</button>
      </div>
    </div>
  );
}
