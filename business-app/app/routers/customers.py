from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.finance import SCORE_CRITERIA, is_valid_mst, lead_score
from app.models import Customer, LeadStatus, User
from app.routers._helpers import templates

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_class=HTMLResponse)
def list_customers(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
    q: str | None = None,
):
    query = db.query(Customer)
    if q:
        query = query.filter(Customer.name.ilike(f"%{q}%"))
    items = query.order_by(Customer.created_at.desc()).all()
    return templates.TemplateResponse(
        "customers/list.html",
        {"request": request, "user": user, "items": items, "q": q or ""},
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        "customers/form.html",
        {"request": request, "user": user, "item": None, "criteria": SCORE_CRITERIA},
    )


@router.post("/new")
def create_customer(
    request: Request,
    name: str = Form(...),
    tax_code: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    has_budget: bool = Form(False),
    decision_maker: bool = Form(False),
    urgent_need: bool = Form(False),
    size_match: bool = Form(False),
    uses_similar: bool = Form(False),
    referral: bool = Form(False),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    tax = tax_code.strip()
    if tax and not is_valid_mst(tax):
        return templates.TemplateResponse(
            "customers/form.html",
            {
                "request": request,
                "user": user,
                "item": None,
                "criteria": SCORE_CRITERIA,
                "error": f"MST '{tax}' không hợp lệ (sai checksum).",
            },
            status_code=400,
        )

    flags = {
        "has_budget": has_budget,
        "decision_maker": decision_maker,
        "urgent_need": urgent_need,
        "size_match": size_match,
        "uses_similar": uses_similar,
        "referral": referral,
    }
    score = lead_score(flags)
    status = LeadStatus.qualified if score >= 70 else LeadStatus.new

    cust = Customer(
        name=name.strip(),
        tax_code=tax or None,
        phone=phone or None,
        email=email or None,
        address=address or None,
        lead_status=status,
        lead_score=score,
    )
    db.add(cust)
    db.commit()
    return RedirectResponse(url="/customers", status_code=303)


@router.post("/{customer_id}/status")
def update_status(
    customer_id: int,
    new_status: LeadStatus = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    cust = db.get(Customer, customer_id)
    if cust:
        cust.lead_status = new_status
        db.commit()
    return RedirectResponse(url="/customers", status_code=303)
