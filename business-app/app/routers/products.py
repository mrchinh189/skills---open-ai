from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Product, User
from app.routers._helpers import templates

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_class=HTMLResponse)
def list_products(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    items = db.query(Product).order_by(Product.sku).all()
    return templates.TemplateResponse(
        "products/list.html", {"request": request, "user": user, "items": items}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        "products/form.html", {"request": request, "user": user, "item": None}
    )


@router.post("/new")
def create_product(
    sku: str = Form(...),
    name: str = Form(...),
    unit: str = Form("cái"),
    price: Decimal = Form(Decimal("0")),
    vat_rate: Decimal = Form(Decimal("10")),
    stock: int = Form(0),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    p = Product(sku=sku, name=name, unit=unit, price=price, vat_rate=vat_rate, stock=stock)
    db.add(p)
    db.commit()
    return RedirectResponse(url="/products", status_code=303)
