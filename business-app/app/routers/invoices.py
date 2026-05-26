from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Invoice, Order, OrderStatus, User
from app.routers._helpers import templates

router = APIRouter(prefix="/invoices", tags=["invoices"])

SERIAL = "1C24TAA"


def _next_number(db: Session) -> str:
    count = db.query(func.count(Invoice.id)).scalar() or 0
    return f"{count + 1:07d}"


@router.get("", response_class=HTMLResponse)
def list_invoices(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    items = db.query(Invoice).order_by(Invoice.issue_date.desc()).all()
    return templates.TemplateResponse(
        "invoices/list.html", {"request": request, "user": user, "items": items}
    )


@router.post("/from-order/{order_id}")
def from_order(
    order_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)
):
    order = db.get(Order, order_id)
    if not order:
        return RedirectResponse(url="/orders", status_code=303)
    inv = Invoice(
        serial=SERIAL,
        number=_next_number(db),
        order_id=order.id,
        customer_id=order.customer_id,
        issue_date=date.today(),
        total=order.total,
        vat_total=order.vat_total,
        grand_total=order.grand_total,
    )
    order.status = OrderStatus.completed
    db.add(inv)
    db.commit()
    return RedirectResponse(url="/invoices", status_code=303)


@router.get("/{invoice_id}", response_class=HTMLResponse)
def detail(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    inv = db.get(Invoice, invoice_id)
    return templates.TemplateResponse(
        "invoices/detail.html",
        {"request": request, "user": user, "inv": inv, "today": datetime.now()},
    )
