from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.finance import compute_vat
from app.models import Customer, Order, OrderItem, OrderStatus, Product, User
from app.routers._helpers import templates

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_class=HTMLResponse)
def list_orders(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    items = db.query(Order).order_by(Order.created_at.desc()).all()
    return templates.TemplateResponse(
        "orders/list.html", {"request": request, "user": user, "items": items}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)):
    customers = db.query(Customer).order_by(Customer.name).all()
    products = db.query(Product).order_by(Product.sku).all()
    return templates.TemplateResponse(
        "orders/form.html",
        {"request": request, "user": user, "customers": customers, "products": products},
    )


@router.post("/new")
async def create_order(
    request: Request,
    customer_id: int = Form(...),
    note: str = Form(""),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    form = await request.form()
    product_ids = form.getlist("product_id")
    quantities = form.getlist("quantity")

    code = "DH-" + datetime.now().strftime("%y%m%d-%H%M%S")
    order = Order(code=code, customer_id=customer_id, status=OrderStatus.draft, note=note or None)
    db.add(order)
    db.flush()

    subtotal = Decimal("0")
    vat_total = Decimal("0")
    for pid_str, qty_str in zip(product_ids, quantities):
        if not pid_str or not qty_str:
            continue
        pid = int(pid_str)
        qty = int(qty_str)
        if qty <= 0:
            continue
        product = db.get(Product, pid)
        if not product:
            continue
        item = OrderItem(
            order_id=order.id,
            product_id=pid,
            quantity=qty,
            unit_price=product.price,
            vat_rate=product.vat_rate,
        )
        db.add(item)
        line_sub = product.price * qty
        subtotal += line_sub
        vat_total += compute_vat(line_sub, product.vat_rate)

    order.total = subtotal
    order.vat_total = vat_total
    order.grand_total = subtotal + vat_total
    db.commit()
    return RedirectResponse(url="/orders", status_code=303)


@router.post("/{order_id}/confirm")
def confirm(order_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    order = db.get(Order, order_id)
    if order and order.status == OrderStatus.draft:
        order.status = OrderStatus.confirmed
        db.commit()
    return RedirectResponse(url="/orders", status_code=303)
