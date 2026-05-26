from __future__ import annotations

from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parents[1]

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.filters["vnd"] = lambda v: f"{int(v):,}".replace(",", ".") if v is not None else "0"
