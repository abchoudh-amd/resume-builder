from pathlib import Path

import click

from resume_builder.parser import load_resume, validate_resume
from resume_builder.renderer import get_available_themes, render_to_file


@click.group()
def cli():
    """YAML Resume Builder -- generate professional resumes from YAML."""
    pass


@cli.command()
@click.option("--input", "input_path", required=True, type=click.Path(exists=True), help="Path to the YAML resume file.")
@click.option("--theme", default="classic", help="Theme name (run 'themes' to list).")
@click.option("--format", "fmt", default="pdf", type=click.Choice(["pdf", "html"]), help="Output format.")
@click.option("--output", "output_path", default=None, help="Output file path (defaults to output/<theme>_resume.<fmt>).")
def build(input_path, theme, fmt, output_path):
    """Build a resume from a YAML file."""
    resume = load_resume(Path(input_path))
    if output_path is None:
        output_path = f"output/{theme}_resume.{fmt}"
    out = Path(output_path)
    render_to_file(resume, theme, out, fmt)
    click.echo(f"Resume generated: {out.resolve()}")


@cli.command()
def themes():
    """List available themes."""
    available = get_available_themes()
    click.echo("Available themes:")
    for t in available:
        click.echo(f"  - {t}")


@cli.command()
@click.option("--input", "input_path", required=True, type=click.Path(exists=True), help="Path to the YAML resume file.")
def validate(input_path):
    """Validate a YAML resume file without rendering."""
    errors = validate_resume(Path(input_path))
    if errors:
        click.echo("Validation errors:", err=True)
        for e in errors:
            click.echo(f"  - {e}", err=True)
        raise SystemExit(1)
    click.echo("YAML resume is valid.")


if __name__ == "__main__":
    cli()
