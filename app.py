from io import BytesIO
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file

from resume_builder.parser import load_resume
from resume_builder.renderer import get_available_themes, render_html, render_pdf

app = Flask(__name__)

SAMPLE_PATH = Path(__file__).parent / "examples" / "sample_resume.yaml"


@app.route("/")
def index():
    sample_yaml = ""
    if SAMPLE_PATH.exists():
        sample_yaml = SAMPLE_PATH.read_text(encoding="utf-8")
    themes = get_available_themes()
    return render_template("index.html", sample_yaml=sample_yaml, themes=themes)


@app.route("/preview", methods=["POST"])
def preview():
    data = request.get_json(silent=True) or {}
    yaml_text = data.get("yaml", "")
    theme = data.get("theme", "classic")
    try:
        resume = load_resume(yaml_text)
        html = render_html(resume, theme)
        return jsonify({"html": html})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    data = request.get_json(silent=True) or {}
    yaml_text = data.get("yaml", "")
    theme = data.get("theme", "classic")
    try:
        resume = load_resume(yaml_text)
        pdf_bytes = render_pdf(resume, theme)
        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{theme}_resume.pdf",
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/download/html", methods=["POST"])
def download_html():
    data = request.get_json(silent=True) or {}
    yaml_text = data.get("yaml", "")
    theme = data.get("theme", "classic")
    try:
        resume = load_resume(yaml_text)
        html = render_html(resume, theme)
        return send_file(
            BytesIO(html.encode("utf-8")),
            mimetype="text/html",
            as_attachment=True,
            download_name=f"{theme}_resume.html",
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/themes")
def list_themes():
    return jsonify(get_available_themes())


if __name__ == "__main__":
    import sys

    if sys.platform == "win32":
        import click._compat, click.utils

        click._compat._default_text_stdout = lambda: sys.stdout
        click._compat._default_text_stderr = lambda: sys.stderr
        click.utils._default_text_stdout = lambda: sys.stdout
        click.utils._default_text_stderr = lambda: sys.stderr

    app.run(debug=True, port=5000)
