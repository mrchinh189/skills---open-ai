from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Attendance, Employee, User
from app.routers._helpers import templates

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("", response_class=HTMLResponse)
def list_records(
    request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)
):
    items = (
        db.query(Attendance).order_by(Attendance.work_date.desc()).limit(100).all()
    )
    employees = db.query(Employee).order_by(Employee.code).all()
    return templates.TemplateResponse(
        "attendance/list.html",
        {"request": request, "user": user, "items": items, "employees": employees},
    )


@router.post("/new")
def create(
    employee_id: int = Form(...),
    work_date: date_type = Form(...),
    hours: Decimal = Form(Decimal("8")),
    ot_hours: Decimal = Form(Decimal("0")),
    note: str = Form(""),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    db.add(
        Attendance(
            employee_id=employee_id,
            work_date=work_date,
            hours=hours,
            ot_hours=ot_hours,
            note=note or None,
        )
    )
    db.commit()
    return RedirectResponse(url="/attendance", status_code=303)
