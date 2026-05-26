from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.db import init_db
from app.routers import (
    agent,
    attendance,
    auth,
    customers,
    documents,
    employees,
    home,
    invoices,
    orders,
    products,
)

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="VBiz Skills Platform", version="0.1.0", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, max_age=60 * 60 * 8)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.exception_handler(303)
async def redirect_to_login(_: Request, __: Exception) -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)


app.include_router(auth.router)
app.include_router(home.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(invoices.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(documents.router)
app.include_router(agent.router)


@app.get("/healthz", response_class=HTMLResponse)
def healthz() -> str:
    return "ok"
