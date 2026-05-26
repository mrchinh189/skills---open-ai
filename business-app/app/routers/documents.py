from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Document, User
from app.routers._helpers import templates

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_class=HTMLResponse)
def list_docs(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
    q: str | None = None,
):
    query = db.query(Document)
    if q:
        query = query.filter(Document.title.ilike(f"%{q}%"))
    items = query.order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(
        "documents/list.html",
        {"request": request, "user": user, "items": items, "q": q or ""},
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        "documents/form.html", {"request": request, "user": user}
    )


@router.post("/new")
def create(
    title: str = Form(...),
    category: str = Form("general"),
    content: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    db.add(Document(title=title, category=category, content=content))
    db.commit()
    return RedirectResponse(url="/documents", status_code=303)


@router.get("/{doc_id}", response_class=HTMLResponse)
def detail(
    doc_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    doc = db.get(Document, doc_id)
    return templates.TemplateResponse(
        "documents/detail.html", {"request": request, "user": user, "doc": doc}
    )
