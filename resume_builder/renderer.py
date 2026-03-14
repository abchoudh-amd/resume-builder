from pathlib import Path
from io import BytesIO
import warnings

from jinja2 import Environment, FileSystemLoader

from .schema import Resume

THEMES_DIR = Path(__file__).resolve().parent.parent / "themes"

DEFAULT_FONT_SIZE_PT = 10.5
MIN_FONT_SIZE_PT = 8.0
FONT_STEP_PT = 0.5
A4_HEIGHT_MM = 297
A4_WIDTH_MM = 210

_weasyprint_available = False
try:
    import sys, os, io
    _devnull = open(os.devnull, "w")
    _real_stdout, _real_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = _devnull, _devnull
    _devnull_fd = os.open(os.devnull, os.O_WRONLY)
    _saved_fd1 = os.dup(1)
    _saved_fd2 = os.dup(2)
    os.dup2(_devnull_fd, 1)
    os.dup2(_devnull_fd, 2)
    os.close(_devnull_fd)
    try:
        from weasyprint import HTML as WeasyprintHTML
        _weasyprint_available = True
    except (ImportError, OSError):
        pass
    finally:
        os.dup2(_saved_fd1, 1)
        os.dup2(_saved_fd2, 2)
        os.close(_saved_fd1)
        os.close(_saved_fd2)
        sys.stdout, sys.stderr = _real_stdout, _real_stderr
        _devnull.close()
except Exception:
    pass


def get_available_themes() -> list[str]:
    return sorted(
        d.name for d in THEMES_DIR.iterdir()
        if d.is_dir() and (d / "template.html").exists()
    )


def render_html(resume: Resume, theme: str, font_size_pt: float | None = None) -> str:
    """Render a Resume to an HTML string using the given theme."""
    if theme not in get_available_themes():
        raise ValueError(f"Unknown theme '{theme}'. Available: {get_available_themes()}")

    env = Environment(
        loader=FileSystemLoader(str(THEMES_DIR / theme)),
        autoescape=True,
    )

    fs = font_size_pt or DEFAULT_FONT_SIZE_PT
    tpl_vars = dict(
        resume=resume,
        fs=fs,
        a4_width_mm=A4_WIDTH_MM,
        a4_height_mm=A4_HEIGHT_MM,
    )

    css_tpl = env.get_template("style.css")
    css = css_tpl.render(**tpl_vars)

    template = env.get_template("template.html")
    return template.render(css=css, **tpl_vars)


def _measure_page_count_weasyprint(html_string: str) -> int:
    doc = WeasyprintHTML(string=html_string).render()
    return len(doc.pages)


def _render_pdf_weasyprint(html_string: str) -> bytes:
    buf = BytesIO()
    WeasyprintHTML(string=html_string).write_pdf(buf)
    return buf.getvalue()


def _render_pdf_xhtml2pdf(html_string: str) -> bytes:
    from xhtml2pdf import pisa
    buf = BytesIO()
    pisa.CreatePDF(html_string, dest=buf)
    return buf.getvalue()


def _auto_scale_html(resume: Resume, theme: str) -> str:
    """Render with progressively smaller font until content fits one page."""
    if not _weasyprint_available:
        return render_html(resume, theme, font_size_pt=DEFAULT_FONT_SIZE_PT)

    fs = DEFAULT_FONT_SIZE_PT
    while fs >= MIN_FONT_SIZE_PT:
        html = render_html(resume, theme, font_size_pt=fs)
        if _measure_page_count_weasyprint(html) <= 1:
            return html
        fs -= FONT_STEP_PT

    html = render_html(resume, theme, font_size_pt=MIN_FONT_SIZE_PT)
    pages = _measure_page_count_weasyprint(html)
    if pages > 1:
        warnings.warn(
            f"Content exceeds one page even at {MIN_FONT_SIZE_PT}pt "
            f"({pages} pages). Consider removing some entries."
        )
    return html


def render_pdf(resume: Resume, theme: str) -> bytes:
    """Render a Resume to PDF bytes. Uses WeasyPrint if available, else xhtml2pdf."""
    html_string = _auto_scale_html(resume, theme)
    if _weasyprint_available:
        return _render_pdf_weasyprint(html_string)
    return _render_pdf_xhtml2pdf(html_string)


def render_to_file(resume: Resume, theme: str, output: Path, fmt: str = "pdf"):
    output.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "pdf":
        output.write_bytes(render_pdf(resume, theme))
    elif fmt == "html":
        output.write_text(render_html(resume, theme), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported format: {fmt}")
