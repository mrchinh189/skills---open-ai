from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.ai import answer, load_skills
from app.auth import current_user
from app.db import get_db
from app.models import Document, User
from app.routers._helpers import templates

router = APIRouter(prefix="/agent", tags=["agent"])


def _retrieve(db: Session, query: str, k: int = 3) -> list[str]:
    """Naive retriever: tìm document chứa từ khoá."""
    terms = [t for t in query.lower().split() if len(t) >= 3]
    if not terms:
        return []
    docs = db.query(Document).all()
    scored: list[tuple[int, Document]] = []
    for d in docs:
        text = (d.title + " " + d.content).lower()
        score = sum(text.count(t) for t in terms)
        if score:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [f"## {d.title}\n{d.content}" for _, d in scored[:k]]


@router.get("", response_class=HTMLResponse)
def chat_page(request: Request, user: User = Depends(current_user)):
    skills = load_skills()
    return templates.TemplateResponse(
        "agent/chat.html",
        {"request": request, "user": user, "skills": skills, "result": None, "query": ""},
    )


@router.post("", response_class=HTMLResponse)
def ask(
    request: Request,
    query: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    docs = _retrieve(db, query)
    result = answer(query, docs)
    skills = load_skills()
    return templates.TemplateResponse(
        "agent/chat.html",
        {
            "request": request,
            "user": user,
            "skills": skills,
            "result": result,
            "query": query,
            "matched_docs": len(docs),
        },
    )
