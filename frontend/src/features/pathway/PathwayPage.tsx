import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { PathwayGraph } from "@/components/pathway/PathwayGraph";
import { TraceTimeline } from "@/components/pathway/TraceTimeline";
import { api } from "@/lib/api/client";

interface RouteItem {
  route: string;
  title: string;
  status: string;
  eligibility: string;
  trace: Array<{ attr: string; op: string; value: unknown; status: string; quote?: string }>;
  caveats: string[];
}

interface PathwayResponse {
  routes: RouteItem[];
  eligible_targets: string[];
  next_questions: string[];
  corpus_version: number;
}

export function PathwayPage() {
  const { t } = useTranslation();
  const [qualType, setQualType] = useState("ITI");
  const [trade, setTrade] = useState("Electrician");
  const [marks, setMarks] = useState("65");
  const [state, setState] = useState("Example State");
  const [selectedRoute, setSelectedRoute] = useState<string | null>("ITI_TO_DIPLOMA_DSE");

  const [response, setResponse] = useState<PathwayResponse>({
    routes: [
      {
        route: "ITI_TO_DIPLOMA_DSE",
        title: "Direct Second Year Diploma (DSE)",
        status: "PASS",
        eligibility: "MEETS_CHECKED_CONDITIONS",
        trace: [
          { attr: "ssc.passed", op: "eq", value: true, status: "PASS", quote: "A candidate who has passed the Class X examination" },
          { attr: "qualification.type", op: "in", value: ["ITI"], status: "PASS", quote: "and holds a Two-Year Craft Certificate" },
          { attr: "craft_certificate.mapped_trade", op: "eq", value: true, status: "PASS", quote: "in a Mapped Trade" },
          { attr: "marks.percent", op: "gte", value: 50.0, status: "PASS", quote: "shall be eligible for Direct Second Year admission" },
        ],
        caveats: ["Subject to seat availability in mapped branch", "Centralized admission choice filling required"],
      },
      {
        route: "ITI_TO_DEGREE_DIRECT",
        title: "Direct Degree (B.Tech) Entry",
        status: "FAIL",
        eligibility: "NOT_ELIGIBLE_UNDER_THIS_RULE",
        trace: [
          { attr: "qualification.type", op: "ne", value: "ITI", status: "FAIL", quote: "Holders of National Trade Certificates (ITI) without a recognised Polytechnic Diploma shall not be admitted directly to Bachelor of Technology or Bachelor of Engineering programmes." },
        ],
        caveats: ["Must first complete polytechnic diploma before lateral entry to B.Tech is possible."],
      },
    ],
    eligible_targets: ["ITI_TO_DIPLOMA_DSE"],
    next_questions: [],
    corpus_version: 1,
  });

  const handleEvaluate = async () => {
    try {
      const res = await api.post<PathwayResponse>("/pathway/check", {
        facts: {
          "ssc.passed": true,
          "qualification.type": qualType,
          "qualification.trade": trade,
          "craft_certificate.mapped_trade": true,
          "marks.percent": parseFloat(marks) || 50.0,
          "state.name": state,
        },
      });
      setResponse(res);
      if (res.routes.length > 0) {
        setSelectedRoute(res.routes[0].route);
      }
    } catch {
      // keep current state
    }
  };

  const currentRoute = response.routes.find((r) => r.route === selectedRoute);

  return (
    <div className="max-w-[1200px] mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="font-display text-[2rem] font-bold text-[var(--primary)]">{t("pathway.title")}</h1>
        <p className="text-sm text-[var(--muted)] mt-1">{t("pathway.disclaimer")}</p>
      </div>

      <div className="grid lg:grid-cols-12 gap-8 items-start">
        {/* Left Form: Student Facts */}
        <div className="lg:col-span-4 bg-[var(--surface)] p-5 rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)] space-y-4">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-[var(--muted)]">Your Educational Facts</h3>
          
          <div>
            <label className="block text-xs font-medium text-[var(--ink)] mb-1">Qualification Type</label>
            <select
              value={qualType}
              onChange={(e) => setQualType(e.target.value)}
              className="w-full text-sm p-2 rounded border border-[var(--border)] bg-[var(--surface)] text-[var(--ink)]"
            >
              <option value="ITI">ITI / National Trade Certificate (2 Years)</option>
              <option value="Diploma">Polytechnic Diploma in Engineering</option>
              <option value="HSC">Class XII (HSC Science / Technical)</option>
              <option value="SSC">Class X (SSC)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-[var(--ink)] mb-1">Trade or Branch</label>
            <select
              value={trade}
              onChange={(e) => setTrade(e.target.value)}
              className="w-full text-sm p-2 rounded border border-[var(--border)] bg-[var(--surface)] text-[var(--ink)]"
            >
              <option value="Electrician">Electrician (2 Years)</option>
              <option value="Electronics Mechanic">Electronics Mechanic (2 Years)</option>
              <option value="Fitter">Fitter (2 Years)</option>
              <option value="Turner">Turner (2 Years)</option>
              <option value="Mechanic Motor Vehicle">Mechanic Motor Vehicle (2 Years)</option>
              <option value="Computer Operator and Programming Assistant">COPA (1 Year)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-[var(--ink)] mb-1">Qualifying Marks Percentage (%)</label>
            <input
              type="number"
              value={marks}
              onChange={(e) => setMarks(e.target.value)}
              min="0"
              max="100"
              className="w-full text-sm p-2 rounded border border-[var(--border)] bg-[var(--surface)] text-[var(--ink)]"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[var(--ink)] mb-1">Domicile State</label>
            <input
              type="text"
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="w-full text-sm p-2 rounded border border-[var(--border)] bg-[var(--surface)] text-[var(--ink)]"
            />
          </div>

          <button
            onClick={handleEvaluate}
            className="w-full py-2.5 bg-[var(--primary)] text-white text-sm font-medium rounded-[var(--r-md)] hover:opacity-90 transition-opacity"
          >
            Evaluate Eligibility Across All Routes
          </button>
        </div>

        {/* Center: Graph */}
        <div className="lg:col-span-4 space-y-4">
          <PathwayGraph
            routes={response.routes}
            selectedRoute={selectedRoute}
            onSelect={(rk) => setSelectedRoute(rk)}
          />
        </div>

        {/* Right: Decision Trace */}
        <div className="lg:col-span-4 bg-[var(--surface)] p-5 rounded-[var(--r-lg)] border border-[var(--border)] shadow-[var(--e1)]">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-[var(--muted)] mb-1">
            Condition Trace
          </h3>
          {currentRoute ? (
            <div>
              <p className="text-sm font-bold text-[var(--primary)] mt-1">{currentRoute.title}</p>
              <TraceTimeline trace={currentRoute.trace} caveats={currentRoute.caveats} />
            </div>
          ) : (
            <p className="text-xs text-[var(--muted)] mt-2">Select a route to view its rule conditions.</p>
          )}
        </div>
      </div>
    </div>
  );
}
