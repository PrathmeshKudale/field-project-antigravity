import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/lib/api/client";
import { setToken } from "@/lib/auth";

export function AuthPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      // Ask backend for the Google consent URL
      const data = await api.get<{ url: string }>("/auth/google/login");
      // Redirect browser to Google's consent screen
      window.location.href = data.url;
    } catch {
      setError("Could not reach the server. Make sure the backend is running on port 8000.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface-2)] px-4">
      <div className="w-full max-w-sm bg-[var(--surface)] rounded-2xl border border-[var(--border)] shadow-[var(--e2)] p-8">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-[var(--primary)] text-white text-2xl font-bold mb-4 shadow-md">
            P
          </div>
          <h1 className="font-display text-2xl font-bold text-[var(--primary)]">ProofPath</h1>
          <p className="text-sm text-[var(--muted)] mt-1">
            Evidence-grounded vocational education answers
          </p>
        </div>

        {/* Google Sign-In */}
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-[var(--border)] rounded-xl bg-white hover:bg-gray-50 text-gray-700 font-medium text-sm shadow-sm transition-all disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? (
            <svg className="animate-spin h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          ) : (
            <GoogleIcon />
          )}
          {loading ? "Redirecting to Google…" : "Continue with Google"}
        </button>

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            {error}
          </div>
        )}

        <p className="text-xs text-[var(--muted)] text-center mt-6 leading-relaxed">
          By signing in you confirm you are a guardian or adult learner reviewing
          vocational education pathways. Your Gmail must be verified by Google.
        </p>

        <div className="mt-6 pt-5 border-t border-[var(--border)] text-center">
          <p className="text-xs text-[var(--muted)]">
            No account needed — sign in with any Gmail address.
          </p>
        </div>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden>
      <path
        fill="#4285F4"
        d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"
      />
      <path
        fill="#34A853"
        d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"
      />
      <path
        fill="#FBBC05"
        d="M3.964 10.71c-.18-.54-.282-1.117-.282-1.71s.102-1.17.282-1.71V4.958H.957C.347 6.173 0 7.548 0 9s.348 2.827.957 4.042l3.007-2.332z"
      />
      <path
        fill="#EA4335"
        d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 6.29C4.672 4.163 6.656 3.58 9 3.58z"
      />
    </svg>
  );
}
