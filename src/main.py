import typer
import os
from pathlib import Path

app = typer.Typer(help="AI Think Tank Command Line Interface")

DOCS_DIR = Path("./docs")
LIBRARY_DIR = DOCS_DIR / "library"
REPORTS_DIR = DOCS_DIR / "reports"
API_DIR = REPORTS_DIR / "API"

@app.command()
def scan_library():
    """
    Scans the docs/library for engineering files and applies OCR/Text parsing (EN/JP).
    """
    typer.echo("🔍 Scanning library for raw engineering documents and military manuals...")
    for root, dirs, files in os.walk(LIBRARY_DIR):
        for file in files:
            if file.endswith(('.pdf', '.png', '.jpg')):
                typer.echo(f"Processing: {file} with JP/EN OCR Engine...")
                # Call your OCR/Translation pipeline here

@app.command()
def ingest_news(topic: str):
    """
    Queries site:mil, site:gov, and site:edu for recent news and triggers the AI engine.
    """
    typer.echo(f"🌐 Fetching official news for topic: '{topic}' from vetted government domains...")
    # Restrict search syntax to strict domains
    vetted_query = f"{topic} (site:gov OR site:mil OR site:edu)"
    typer.echo(f"Running automated discovery on: {vetted_query}")
    # Run intelligence gathering and save .md solutions to REPORTS_DIR

@app.command()
def export_joomla():
    """
    Processes finished reports into Joomla 6 compatible HTML API structures.
    """
    typer.echo("📦 Categorizing solutions and packaging HTML payloads for Joomla 6 Web Services API...")
    # Map markdown files to Joomla Category schemas, convert to HTML, and drop into API_DIR
    typer.echo(f"Export payloads updated in {API_DIR}")

if __name__ == "__main__":
    app()
