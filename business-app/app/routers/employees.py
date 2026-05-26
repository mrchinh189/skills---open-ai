from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.finance import compute_payroll
from app.models import Employee, User
from app.routers._helpers import templates

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_class=HTMLResponse)
def list_employees(
    request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)
):
    items = db.query(Employee).order_by(Employee.code).all()
    return templates.TemplateResponse(
        "employees/list.html", {"request": request, "user": user, "items": items}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        "employees/form.html", {"request": request, "user": user}
    )


@router.post("/new")
def create(
    code: str = Form(...),
    full_name: str = Form(...),
    position: str = Form(""),
    department: str = Form(""),
    base_salary: Decimal = Form(Decimal("0")),
    dependents: int = Form(0),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    emp = Employee(
        code=code,
        full_name=full_name,
        position=position or None,
        department=department or None,
        base_salary=base_salary,
        dependents=dependents,
        joined_at=date.today(),
    )
    db.add(emp)
    db.commit()
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/{employee_id}/payroll", response_class=HTMLResponse)
def payroll(
    employee_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
    days: Decimal = Decimal("22"),
    ot_n: Decimal = Decimal("0"),
    ot_w: Decimal = Decimal("0"),
    ot_h: Decimal = Decimal("0"),
):
    emp = db.get(Employee, employee_id)
    result = (
        compute_payroll(
            base_salary=emp.base_salary,
            days_worked=days,
            ot_normal_hours=ot_n,
            ot_weekend_hours=ot_w,
            ot_holiday_hours=ot_h,
            dependents=emp.dependents,
        )
        if emp
        else None
    )
    return templates.TemplateResponse(
        "employees/payroll.html",
        {
            "request": request,
            "user": user,
            "emp": emp,
            "result": result,
            "days": days,
            "ot_n": ot_n,
            "ot_w": ot_w,
            "ot_h": ot_h,
        },
    )
