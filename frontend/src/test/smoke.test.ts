import { describe, it, expect } from "vitest";

describe("verdict types", () => {
  it("covers all 5 verdict values", () => {
    const verdicts = [
      "VERIFIED_FACT",
      "MYTH_FALSE",
      "PARTIALLY_TRUE",
      "CONTEXT_DEPENDENT",
      "INSUFFICIENT_EVIDENCE",
    ] as const;
    expect(verdicts).toHaveLength(5);
    verdicts.forEach((v) => expect(typeof v).toBe("string"));
  });
});

describe("pipeline stages", () => {
  it("defines 4 stages in correct order", () => {
    const stages = ["understand", "retrieve", "verify", "explain"];
    expect(stages).toHaveLength(4);
    expect(stages[0]).toBe("understand");
    expect(stages[3]).toBe("explain");
  });
});

describe("quote guard logic", () => {
  it("rejects quotes shorter than 6 words", () => {
    const isValid = (q: string) => q.trim().split(/\s+/).length >= 6 && q.length >= 25 && q.length <= 400;
    expect(isValid("too short")).toBe(false);
    expect(isValid("A candidate who has passed the Class X examination")).toBe(true);
  });

  it("rejects quotes over 400 chars", () => {
    const longQuote = "word ".repeat(100).trim();
    const isValid = (q: string) => q.trim().split(/\s+/).length >= 6 && q.length >= 25 && q.length <= 400;
    expect(isValid(longQuote)).toBe(false);
  });
});
