import React from "react";
import { useTranslation } from "react-i18next";
import { ReportSheet } from "@/components/layout/ReportSheet";

export function ReportPage() {
  const { t } = useTranslation();
  return (
    <div className="max-w-[1200px] mx-auto px-4 py-8">
      <h1 className="font-display text-[2rem] font-bold text-[var(--primary)] mb-6">{t("report.title")}</h1>
      <div className="p-8 bg-[var(--surface)] rounded-[var(--r-lg)] border border-[var(--border)] text-center text-[var(--muted)]">
        <p className="text-base text-[var(--ink)] mb-2 font-medium">No saved reports yet.</p>
        <p className="text-sm">Ask a question on the home screen and click "Save & Print Family Report" to store official verification results here.</p>
      </div>
    </div>
  );
}
