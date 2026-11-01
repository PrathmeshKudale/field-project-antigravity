export function formatDate(date: string | null | undefined, locale = "en-IN"): string {
  if (!date) return "—";
  try {
    return new Intl.DateTimeFormat(locale, { day: "numeric", month: "short", year: "numeric" }).format(new Date(date));
  } catch {
    return date;
  }
}

export function formatPercent(value: number): string {
  return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 1 }).format(value) + "%";
}

export function freshnessStatus(effectiveUntil: string | null | undefined): "current" | "expiring" | "stale" | "superseded" {
  if (!effectiveUntil) return "current";
  const days = (new Date(effectiveUntil).getTime() - Date.now()) / (1000 * 60 * 60 * 24);
  if (days < 0) return "stale";
  if (days < 60) return "expiring";
  return "current";
}
