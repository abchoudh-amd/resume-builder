from pathlib import Path

import yaml
from pydantic import ValidationError

from .schema import Resume


def load_resume(source: str | Path) -> Resume:
    """Load and validate a resume from a YAML file path or raw YAML string."""
    if isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
        text = Path(source).read_text(encoding="utf-8")
    else:
        text = source

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("YAML must be a mapping at the top level")
    return Resume(**data)


def validate_resume(source: str | Path) -> list[str]:
    """Return a list of validation error messages, or an empty list if valid."""
    try:
        load_resume(source)
        return []
    except ValidationError as exc:
        return [str(e) for e in exc.errors()]
    except Exception as exc:
        return [str(exc)]
