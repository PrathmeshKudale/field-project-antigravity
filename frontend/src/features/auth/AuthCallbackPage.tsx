import React, { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { setToken } from "@/lib/auth";

const API_BASE = "/api/v1";

/**
 * Google redirects here after consent: /auth/callback?code=XXX
 * Exchange code with backend ONCE, store JWT, redirect to home.
 */
export function AuthCallbackPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<"loading" | "error">("loading");
  const [errMsg, setErrMsg] = useState("");
  const calledRef = useRef(false); // prevent double-call in React StrictMode

  useEffect(() => {
    if (calledRef.current) return;
    calledRef.current = true;

    const code = searchParams.get("code");
    const error = searchParams.get("error");

    if (error) {
      setErrMsg(`Google declined: ${error}`);
      setStatus("error");
      return;
    }
    if (!code) {
      setErrMsg("No authorisation code received from Google.");
      setStatus("error");
      return;
    }

    // Exchange code with our backend — fire once only
    fetch(`${API_BASE}/auth/google/callback?code=${encodeURIComponent(code)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then(async (res) => {
        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: "Unknown error" }));
          throw new Error(err.detail ?? `HTTP ${res.status}`);
        }
        return res.json() as Promise<{ access_token: string; role: string; language: string }>;
      })
      .then((data) => {
        setToken(data.access_token);
        navigate("/", { replace: true });
      })
      .catch((err: Error) => {
        setErrMsg(err.message || "Authentication failed. Please try again.");
        setStatus("error");
      });
  }, []); // empty deps — run once on mount only

  if (status === "loading") {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[var(--surface-2)] gap-4">
        <svg className="animate-spin h-10 w-10 text-[var(--accent)]" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <p className="text-[var(--muted)] text-sm font-medium">Verifying your Gmail with Google…</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[var(--surface-2)] px-4">
      <div className="w-full max-w-sm bg-[var(--surface)] rounded-2xl border border-red-200 shadow-[var(--e1)] p-8 text-center">
        <div className="text-4xl mb-4">⚠️</div>
        <h2 className="font-display text-xl font-bold text-red-700 mb-2">Sign-in Failed</h2>
        <p className="text-sm text-[var(--muted)] mb-6">{errMsg}</p>
        <button
          onClick={() => navigate("/auth")}
          className="px-6 py-2 bg-[var(--primary)] text-white rounded-xl font-medium text-sm hover:opacity-90"
        >
          Try Again
        </button>
      </div>
    </div>
  );
}
