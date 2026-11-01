export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        "surface-2": "var(--surface-2)",
        border: "var(--border)",
        ink: "var(--ink)",
        muted: "var(--muted)",
        primary: "var(--primary)",
        accent: "var(--accent)",
        v: {
          verified: { fg: "var(--v-verified-fg)", bg: "var(--v-verified-bg)" },
          myth: { fg: "var(--v-myth-fg)", bg: "var(--v-myth-bg)" },
          partial: { fg: "var(--v-partial-fg)", bg: "var(--v-partial-bg)" },
          context: { fg: "var(--v-context-fg)", bg: "var(--v-context-bg)", line: "var(--v-context-line)" },
          insuff: { fg: "var(--v-insuff-fg)", bg: "var(--v-insuff-bg)" },
        },
      },
      fontFamily: {
        display: ["Fraunces Variable", "Georgia", "serif"],
        sans: ["Inter Variable", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono Variable", "ui-monospace", "monospace"],
      },
      borderRadius: {
        sm: "6px",
        md: "10px",
        lg: "16px",
      },
      boxShadow: {
        e1: "var(--e1)",
        e2: "var(--e2)",
      },
    },
  },
};
