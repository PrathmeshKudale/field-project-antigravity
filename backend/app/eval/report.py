"""Export Eval Lab results as Markdown table and CSV."""


def format_markdown_report(eval_results: dict) -> str:
    md = """# ProofPath Evaluation Report
Corpus Mode: demo | Benchmark Items: {total}

| System | Unsupported Rate (lower better) | Citation Precision | Verdict Accuracy | Abstention F1 |
|---|---|---|---|---|
""".format(total=eval_results.get("benchmark_count", 0))

    for sys_key, data in eval_results.get("systems", {}).items():
        md += f"| **{data['name']}** | {data.get('unsupported_rate', 0):.2f} | {data.get('citation_precision', 0):.2f} | {data.get('verdict_accuracy', 0):.2f} | {data.get('abstention_f1', 0):.2f} |\n"

    return md
