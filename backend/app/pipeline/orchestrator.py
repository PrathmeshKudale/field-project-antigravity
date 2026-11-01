import uuid
import json
import logging
from pathlib import Path

from app.pipeline.pii import scrub
from app.pipeline.understand import heuristic_understand
from app.pipeline.verify import verify_claims_against_chunks
from app.pipeline.quote_guard import validate
from app.pipeline.aggregate import aggregate, ClaimItem, Verdict
from app.pipeline.explain import render_template_explanation
from app.retrieval.hybrid import search_hybrid
from app.rules.engine import evaluate_rule, EligibilityStatus
from app.rules.next_question import compute_next_questions
from app.schemas.ask import AskResponse, ClaimResult, EvidencePassport
from app.llm.gemini import generate_content_gemini
from app.core.config import settings

logger = logging.getLogger("proofpath.pipeline")


def load_demo_rules() -> list[dict]:
    p = Path("d:/field_project_1/student-1/data/demo/rules.demo.json")
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("rules", [])
    return []


def process_question(question: str) -> AskResponse:
    """Run the complete ProofPath verification pipeline augmented by Gemini 1.5."""
    # Stage 0: Guard & PII scrub (Invariant 7: No PII sent to external LLMs)
    scrubbed_q = scrub(question)

    # Stage 1: Understand
    understand_out = heuristic_understand(scrubbed_q)

    # Stage 2: Retrieve relevant policy passages (Hybrid vector + FTS)
    chunks = search_hybrid(scrubbed_q, top_k=8)

    # Stage 3: Verify (Extract atomic claims & match against retrieved passages)
    raw_verifications = verify_claims_against_chunks(understand_out.atomic_claims, chunks)

    # Stage 4: Quote guard (Invariant 3: deterministic validation of quotes against chunk text)
    claim_items = []
    claim_results = []
    evidence_passports = []

    for v in raw_verifications:
        chunk_text = ""
        chunk_page = 1
        chunk_clause = None
        for c in chunks:
            if str(c.get("id")) == str(v.chunk_id):
                chunk_text = c.get("text", "")
                chunk_page = c.get("page_number", 1)
                chunk_clause = c.get("clause_ref")
                break

        is_valid = validate(v.quote or "", chunk_text) if (v.quote and chunk_text) else False
        stance = v.stance if is_valid else "none"

        claim_items.append(ClaimItem(
            claim=v.claim,
            stance=stance,
            chunk_id=v.chunk_id,
            quote=v.quote,
            quote_valid=is_valid,
        ))

        claim_results.append(ClaimResult(
            claim=v.claim,
            stance=stance,
            chunk_id=v.chunk_id,
            quote=v.quote,
            quote_valid=is_valid,
            source_id="demo-handbook-2026",
            source_title="Admission Handbook 2026-27",
            page_number=chunk_page,
        ))

        if v.quote and is_valid:
            evidence_passports.append(EvidencePassport(
                authority="Example State Board (DEMO)",
                document="Admission Handbook 2026-27",
                version="v1",
                page=chunk_page,
                clause=chunk_clause,
                quote=v.quote,
                quote_valid=True,
                freshness_status="current",
                effective_until="2027-05-31",
                source_url="https://example.gov.in/handbook2026.pdf",
                corpus_version=1,
            ))

    # Stage 5: Rule engine (Invariant 2: Deterministic 3-valued Kleene engine decides eligibility)
    all_rules = load_demo_rules()
    eval_results = []
    for r in all_rules:
        eval_results.append(evaluate_rule(r, understand_out.extracted_facts))

    next_qs = compute_next_questions(eval_results, understand_out.extracted_facts)

    # Stage 6: Aggregator (Pure code aggregation into 5 verdicts)
    verdict = aggregate(
        claim_items,
        needs_rule_engine=understand_out.needs_rule_engine,
        out_of_scope=understand_out.out_of_scope,
    )

    # Stage 7: Explain synthesis (AI augmented with Gemini if available, fallback to templates)
    explanation: list[str] = []
    summary: str = ""

    # Check if live Gemini API key is configured
    if settings.gemini_api_key:
        valid_quotes = [f"Clause: {e.clause or ''} - Quote: \"{e.quote}\"" for e in evidence_passports]
        quotes_context = "\n".join(valid_quotes) if valid_quotes else "No direct quote available."

        system_prompt = (
            "You are ProofPath's explanation generator for student vocational pathways.\n"
            "INVARIANTS:\n"
            "1. You NEVER decide eligibility. The verdict is already decided: " + verdict.value + ".\n"
            "2. Never guarantee admission, job, salary, or placement.\n"
            "3. Ground all statements only in the provided verified quotes.\n"
            "Respond in JSON format with two keys:\n"
            " 'summary': A clear 1-2 sentence overview of the verdict.\n"
            " 'points': An array of 2-4 bullet strings explaining the criteria and rules.\n"
        )

        user_prompt = f"""
<source_data>
Question: {scrubbed_q}
Determined Verdict: {verdict.value}
Verified Quotes from Official Sources:
{quotes_context}
</source_data>
Synthesize the explanation for the user following the JSON schema.
"""
        raw_ai = generate_content_gemini(
            prompt=user_prompt,
            system_instruction=system_prompt,
            json_mode=True,
            model=settings.llm_model or "gemini-1.5-flash",
        )

        if raw_ai:
            try:
                ai_data = json.loads(raw_ai)
                if isinstance(ai_data.get("summary"), str):
                    summary = ai_data["summary"]
                if isinstance(ai_data.get("points"), list):
                    explanation = [str(p) for p in ai_data["points"] if p]
            except Exception as e:
                logger.warning(f"Failed to parse Gemini explanation response: {e}")

    # Fallback to deterministic templates if Gemini isn't active or fails
    if not explanation:
        explanation = render_template_explanation(verdict.value, language=understand_out.language)

    if not summary:
        summary_map = {
            "VERIFIED_FACT": "Supported by official documents and state eligibility rules on record.",
            "MYTH_FALSE": "Sources state that standalone ITI does not provide direct entry to B.Tech programmes.",
            "PARTIALLY_TRUE": "Partly true: eligibility depends on trade mapping and board recognition.",
            "CONTEXT_DEPENDENT": "ITI and polytechnic diploma are separate pathways. Eligibility depends on your specific trade and marks.",
            "INSUFFICIENT_EVIDENCE": "Our approved official sources do not establish an answer to this question.",
        }
        summary = summary_map.get(verdict.value, "Decision support based on official state guidelines.")

    return AskResponse(
        answer_id=str(uuid.uuid4())[:12],
        verdict=verdict.value,
        summary=summary,
        claims=claim_results,
        evidence=evidence_passports,
        explanation=explanation,
        next_questions=next_qs,
        corpus_version=1,
        review_flag=False,
        language=understand_out.language,
    )
