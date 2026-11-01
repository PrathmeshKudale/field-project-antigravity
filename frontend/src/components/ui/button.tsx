import { clsx } from "clsx";
import React, { ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "md", ...props }, ref) => (
    <button
      ref={ref}
      className={clsx(
        "inline-flex items-center justify-center rounded-[var(--r-md)] font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)]",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        size === "sm" && "px-3 py-1.5 text-xs",
        size === "md" && "px-4 py-2 text-sm",
        size === "lg" && "px-5 py-2.5 text-base",
        variant === "default" && "bg-[var(--primary)] text-white hover:opacity-90",
        variant === "outline" && "border border-[var(--border)] bg-transparent hover:bg-[var(--surface-2)] text-[var(--ink)]",
        variant === "ghost" && "hover:bg-[var(--surface-2)] text-[var(--muted)]",
        variant === "destructive" && "bg-[var(--v-myth-fg)] text-white hover:opacity-90",
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
