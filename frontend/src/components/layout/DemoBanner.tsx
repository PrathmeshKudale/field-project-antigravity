import React from "react";
import { AlertTriangle } from "lucide-react";
import { useTranslation } from "react-i18next";

interface DemoBannerProps {
  visible: boolean;
}

export function DemoBanner({ visible }: DemoBannerProps) {
  const { t } = useTranslation();
  if (!visible) return null;
  return (
    <div
      role="alert"
      className="w-full bg-[var(--v-context-bg)] border-b border-[var(--v-context-line)] text-[var(--v-context-fg)] px-4 py-2 text-center text-xs sm:text-sm font-medium flex items-center justify-center gap-2"
    >
      <AlertTriangle size={15} aria-hidden />
      <span>{t("demo_banner")}</span>
    </div>
  );
}
