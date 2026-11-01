import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { AskPage } from "@/features/ask/AskPage";
import { PathwayPage } from "@/features/pathway/PathwayPage";
import { ReportPage } from "@/features/report/ReportPage";
import { AuthPage } from "@/features/auth/AuthPage";
import { AuthCallbackPage } from "@/features/auth/AuthCallbackPage";
import { StudioPage } from "@/features/studio/StudioPage";
import { EvalPage } from "@/features/eval/EvalPage";
import { SourcesPage } from "@/features/sources/SourcesPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <AskPage /> },
      { path: "pathway", element: <PathwayPage /> },
      { path: "reports", element: <ReportPage /> },
      { path: "auth", element: <AuthPage /> },
      { path: "auth/callback", element: <AuthCallbackPage /> },
      { path: "studio", element: <StudioPage /> },
      { path: "eval", element: <EvalPage /> },
      { path: "sources", element: <SourcesPage /> },
    ],
  },
]);
