from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Customer, Employee, Invoice, Order, Product, User
from app.routers._helpers import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    stats = {
        "customers": db.query(func.count(Customer.id)).scalar() or 0,
        "products": db.query(func.count(Product.id)).scalar() or 0,
        "orders": db.query(func.count(Order.id)).scalar() or 0,
        "invoices": db.query(func.count(Invoice.id)).scalar() or 0,
        "employees": db.query(func.count(Employee.id)).scalar() or 0,
        "revenue": db.query(func.coalesce(func.sum(Invoice.grand_total), 0)).scalar() or 0,
    }
    recent_orders = (
        db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    )
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "stats": stats, "recent_orders": recent_orders},
    )
