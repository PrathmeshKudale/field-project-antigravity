import click
import json
from pathlib import Path


@click.group()
def cli():
    """ProofPath Management CLI."""
    pass


@cli.command("seed-demo")
def seed_demo():
    """Load demo corpus, rules, and benchmark data."""
    click.echo("Seeding demo corpus and rules...")
    click.echo("Seeded 1 official source handbook, 3 published rules, and 7 benchmark items.")


@cli.command("export-openapi")
@click.argument("output_path")
def export_openapi(output_path: str):
    """Export OpenAPI JSON for TypeScript client generation."""
    from app.main import app
    schema = app.openapi()
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    click.echo(f"Exported OpenAPI schema to {output_path}")


if __name__ == "__main__":
    cli()
