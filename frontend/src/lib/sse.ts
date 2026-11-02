export type SSEEvent =
  | { type: "stage"; stage: string; label: string }
  | {
      type: "result";
      verdict: string;
      summary: string;
      claims: Array<{
        claim: string;
        stance: "supports" | "contradicts" | "partial" | "none";
        chunk_id: string | null;
        quote: string | null;
        quote_valid: boolean;
      }>;
      evidence: Array<{
        authority: string;
        document: string;
        version: string;
        page: number;
        clause: string | null;
        quote: string;
        quote_valid: boolean;
        freshness_status: string;
        effective_until: string | null;
        source_url: string | null;
        corpus_version: number;
      }>;
      explanation: string[];
      next_questions: string[];
      corpus_version: number;
      language: string;
    }
  | { type: "error"; message: string };

export async function streamAsk(
  question: string,
  onEvent: (evt: SSEEvent) => void,
  signal?: AbortSignal
): Promise<void> {
  const apiBase = import.meta.env.VITE_API_URL || "";
  const url = `${apiBase}/api/v1/ask/stream?question=${encodeURIComponent(question)}`;
  const response = await fetch(url, { signal });
  if (!response.ok || !response.body) {
    throw new Error(`HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = line.slice(6).trim();
        if (data === "[DONE]") return;
        try {
          const evt = JSON.parse(data) as SSEEvent;
          onEvent(evt);
        } catch {
          // ignore malformed lines
        }
      }
    }
  }
}
