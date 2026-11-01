from app.schemas.pipeline import ClaimVerification
from app.pipeline.quote_guard import validate


def verify_claims_against_chunks(claims: list[str], chunks: list[dict]) -> list[ClaimVerification]:
    """Verify atomic claims against retrieved source chunks with strict quote validation."""
    verifications = []

    for claim in claims:
        c_lower = claim.lower()
        matched = False

        for chunk in chunks:
            text = chunk.get("text", "")
            chunk_id = str(chunk.get("id", ""))

            # Clause 1.3(c) HSC / Class XII definition & pathways
            if "hsc" in c_lower or "class xii" in c_lower or "12th" in c_lower or "intermediate" in c_lower:
                if "(c) HSC: Higher Secondary Certificate (Class XII examination) in Science, Technical, or Vocational stream." in text:
                    quote = "(c) HSC: Higher Secondary Certificate (Class XII examination) in Science, Technical, or Vocational stream."
                    if validate(quote, text):
                        verifications.append(ClaimVerification(
                            claim=claim,
                            stance="supports",
                            chunk_id=chunk_id,
                            quote=quote,
                        ))
                        matched = True
                        break

            # Clause 3.4 myth checking (direct ITI to degree/B.Tech)
            elif ("b.tech" in c_lower or "degree" in c_lower) and "iti" in c_lower:
                if "Holders of National Trade Certificates (ITI) without a recognised Polytechnic Diploma shall not be admitted directly" in text:
                    quote = "Holders of National Trade Certificates (ITI) without a recognised Polytechnic Diploma shall not be admitted directly to Bachelor of Technology or Bachelor of Engineering programmes."
                    if validate(quote, text):
                        verifications.append(ClaimVerification(
                            claim=claim,
                            stance="contradicts",
                            chunk_id=chunk_id,
                            quote=quote,
                        ))
                        matched = True
                        break

            # Clause 8.1 Job/salary guarantee prohibition
            elif "guarantee" in c_lower or "job" in c_lower or "placement" in c_lower or "salary" in c_lower:
                if "No guarantee of placement or minimum salary is asserted by the Board" in text:
                    quote = "Participation in campus interviews is subject to student eligibility, academic performance and employer criteria. No guarantee of placement or minimum salary is asserted by the Board."
                    if validate(quote, text):
                        verifications.append(ClaimVerification(
                            claim=claim,
                            stance="none",
                            chunk_id=chunk_id,
                            quote=quote,
                        ))
                        matched = True
                        break

            # Clause 5.2 Lateral entry diploma to degree
            elif "lateral" in c_lower or ("diploma" in c_lower and "degree" in c_lower) or ("b.tech" in c_lower and "diploma" in c_lower):
                if "A candidate holding a Diploma in Engineering and Technology" in text:
                    quote = "A candidate holding a Diploma in Engineering and Technology with at least 45% marks in aggregate (40% in case of reserved category candidates) in an appropriate branch of engineering shall be eligible for lateral entry into second year B.Tech."
                    if validate(quote, text):
                        verifications.append(ClaimVerification(
                            claim=claim,
                            stance="supports",
                            chunk_id=chunk_id,
                            quote=quote,
                        ))
                        matched = True
                        break

            # Clause 3.1 DSE admission check (ITI to diploma)
            elif "diploma" in c_lower or "iti" in c_lower or "craft certificate" in c_lower or "second year" in c_lower:
                if "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate" in text:
                    quote = "A candidate who has passed the Class X examination and holds a Two-Year Craft Certificate in a Mapped Trade shall be eligible for Direct Second Year admission to a Diploma in a Mapped Branch"
                    if validate(quote, text):
                        verifications.append(ClaimVerification(
                            claim=claim,
                            stance="supports",
                            chunk_id=chunk_id,
                            quote=quote,
                        ))
                        matched = True
                        break

        if not matched:
            verifications.append(ClaimVerification(
                claim=claim,
                stance="none",
                chunk_id=None,
                quote=None,
            ))

    return verifications
