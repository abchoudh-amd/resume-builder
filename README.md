# YAML Resume Builder

Generate professional single-page PDF and HTML resumes from YAML data with 5 modern themes.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## Usage

### CLI

```bash
# Build a PDF resume
python cli.py build --input examples/sample_resume.yaml --theme modern --format pdf --output output/resume.pdf

# Build an HTML resume
python cli.py build --input examples/sample_resume.yaml --theme classic --format html --output output/resume.html

# List available themes
python cli.py themes

# Validate YAML without rendering
python cli.py validate --input examples/sample_resume.yaml
```

### Web UI

```bash
python app.py
```

Open `http://localhost:5000` in your browser. Edit YAML on the left, see a live preview on the right, and download PDF or HTML.

## Themes

| Theme | Style |
|-------|-------|
| classic | Two-column, serif fonts, navy headings, ATS-friendly |
| modern | Teal sidebar, skill bars, sans-serif |
| minimal | Single-column, monochrome, maximum whitespace |
| bold | Indigo header block, timeline experience, pill badges |
| elegant | Warm taupe accent, cream background, data-dense |

## YAML Format

See `examples/sample_resume.yaml` for the full schema. Sections: `personal`, `experience`, `education`, `skills`, `projects`.
