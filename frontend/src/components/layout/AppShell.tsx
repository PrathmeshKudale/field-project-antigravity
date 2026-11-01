import React, { useState, useEffect } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { Sun, Moon, Globe, Menu, X, BookOpen, LogOut, User } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import { getToken, clearToken } from "@/lib/auth";
import { clsx } from "clsx";

interface CorpusMeta {
  corpus_mode: string;
  corpus_version: number;
  last_updated: string;
}

interface UserProfile {
  id: string;
  email: string;
  role: string;
  language: string;
}

export function AppShell() {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [dark, setDark] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [token, setTokenState] = useState<string | null>(getToken());

  const { data: meta } = useQuery<CorpusMeta>({
    queryKey: ["corpus-meta"],
    queryFn: () => api.get<CorpusMeta>("/meta/corpus"),
    staleTime: 5 * 60 * 1000,
  });

  const { data: user } = useQuery<UserProfile>({
    queryKey: ["me", token],
    queryFn: () => api.get<UserProfile>("/auth/me"),
    enabled: !!token,
    retry: false,
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const toggleLang = () => {
    const next = i18n.language === "en" ? "hinglish" : "en";
    i18n.changeLanguage(next);
  };

  const handleSignOut = () => {
    clearToken();
    setTokenState(null);
    navigate("/auth");
  };

  const navLinks = [
    { to: "/", label: t("nav.ask"), end: true },
    { to: "/pathway", label: t("nav.pathway") },
    { to: "/reports", label: t("nav.reports") },
    { to: "/studio", label: t("nav.studio") },
    { to: "/eval", label: t("nav.eval") },
    { to: "/sources", label: t("nav.sources") },
  ];

  const isLiveMode = meta?.corpus_mode !== "demo";

  return (
    <div className="min-h-screen bg-[var(--bg)] flex flex-col text-[var(--ink)]">
      <a href="#main-content" className="skip-to-content">{t("nav.ask")}</a>

      {/* Demo banner — only shown in demo mode */}
      {meta?.corpus_mode === "demo" && (
        <div className="bg-amber-500 text-white text-xs font-semibold text-center py-2 px-4">
          ⚠ DEMO DATA — Answers are based on illustrative policy documents, not real state board rules.
        </div>
      )}

      <header className="sticky top-0 z-50 bg-[var(--surface)] border-b border-[var(--border)] shadow-[var(--e1)]">
        <div className="max-w-[1200px] mx-auto px-4 h-14 flex items-center justify-between">
          <NavLink to="/" className="font-display text-xl font-bold text-[var(--primary)] flex items-center gap-2">
            <BookOpen size={20} className="text-[var(--accent)]" />
            ProofPath
            {isLiveMode && (
              <span className="text-[10px] font-bold bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full ml-1">LIVE</span>
            )}
          </NavLink>

          <nav aria-label="Main navigation" className="hidden md:flex items-center gap-6">
            {navLinks.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  clsx(
                    "text-sm font-medium transition-colors hover:text-[var(--accent)]",
                    isActive ? "text-[var(--accent)] font-semibold border-b-2 border-[var(--accent)] pb-1" : "text-[var(--muted)]"
                  )
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <button
              onClick={toggleLang}
              aria-label="Toggle language"
              className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border border-[var(--border)] text-[var(--ink)] hover:border-[var(--accent)] font-medium"
            >
              <Globe size={13} aria-hidden />
              {i18n.language === "en" ? "EN" : "Hinglish"}
            </button>
            <button
              onClick={() => setDark(!dark)}
              aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
              className="p-2 rounded-full hover:bg-[var(--surface-2)] text-[var(--muted)]"
            >
              {dark ? <Sun size={17} aria-hidden /> : <Moon size={17} aria-hidden />}
            </button>

            {/* Auth: signed in → avatar + sign out; else → Sign In button */}
            {user ? (
              <div className="hidden sm:flex items-center gap-2">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--surface-2)] border border-[var(--border)]">
                  <User size={13} className="text-[var(--accent)]" aria-hidden />
                  <span className="text-xs font-medium text-[var(--ink)] max-w-[120px] truncate">
                    {user.email}
                  </span>
                </div>
                <button
                  onClick={handleSignOut}
                  className="p-2 rounded-full hover:bg-[var(--surface-2)] text-[var(--muted)]"
                  aria-label="Sign out"
                  title="Sign out"
                >
                  <LogOut size={15} aria-hidden />
                </button>
              </div>
            ) : (
              <NavLink
                to="/auth"
                className="text-xs px-3 py-1.5 rounded-[var(--r-md)] bg-[var(--primary)] text-white font-medium hover:opacity-90 hidden sm:inline-flex items-center gap-1.5"
              >
                Sign In with Google
              </NavLink>
            )}

            <button
              className="md:hidden p-2 rounded hover:bg-[var(--surface-2)] text-[var(--muted)]"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label={menuOpen ? "Close menu" : "Open menu"}
            >
              {menuOpen ? <X size={20} aria-hidden /> : <Menu size={20} aria-hidden />}
            </button>
          </div>
        </div>

        {menuOpen && (
          <nav aria-label="Mobile navigation" className="md:hidden border-t border-[var(--border)] bg-[var(--surface)] px-4 py-3 space-y-2">
            {navLinks.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={() => setMenuOpen(false)}
                className={({ isActive }) =>
                  clsx("block py-2 text-sm font-medium", isActive ? "text-[var(--accent)] font-semibold" : "text-[var(--muted)]")
                }
              >
                {item.label}
              </NavLink>
            ))}
            <div className="pt-2 border-t border-[var(--border)]">
              {user ? (
                <button
                  onClick={handleSignOut}
                  className="block w-full text-center py-2 text-sm text-red-600 font-medium"
                >
                  Sign Out ({user.email})
                </button>
              ) : (
                <NavLink
                  to="/auth"
                  onClick={() => setMenuOpen(false)}
                  className="block text-center py-2 text-sm bg-[var(--primary)] text-white rounded font-medium"
                >
                  Sign In with Google
                </NavLink>
              )}
            </div>
          </nav>
        )}
      </header>

      <main id="main-content" className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-[var(--border)] bg-[var(--surface)] py-4">
        <div className="max-w-[1200px] mx-auto px-4 flex flex-col sm:flex-row items-center justify-between text-xs text-[var(--muted)] gap-2">
          <span>{t("footer_disclaimer")}</span>
          {meta && (
            <span>
              Corpus: v{meta.corpus_version} ({meta.corpus_mode}) · Updated: {meta.last_updated}
            </span>
          )}
        </div>
      </footer>
    </div>
  );
}
