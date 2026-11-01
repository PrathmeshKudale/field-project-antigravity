import React, { ReactNode } from "react";
import { clsx } from "clsx";

interface BadgeProps {
  children: ReactNode;
  className?: string;
  variant?: "default" | "success" | "warning" | "error";
}

export function Badge({ children, className, variant = "default" }: BadgeProps) {
  return (
    <span className={clsx(
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
      variant === "default" && "bg-[var(--surface-2)] text-[var(--muted)]",
      variant === "success" && "bg-[var(--v-verified-bg)] text-[var(--v-verified-fg)]",
      variant === "warning" && "bg-[var(--v-context-bg)] text-[var(--v-context-fg)]",
      variant === "error" && "bg-[var(--v-myth-bg)] text-[var(--v-myth-fg)]",
      className
    )}>
      {children}
    </span>
  );
}
