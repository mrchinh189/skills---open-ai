from __future__ import annotations

import os
import tempfile

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_vbiz.db")
os.environ.setdefault("SECRET_KEY", "test-secret-test-test-test-test-test")


@pytest.fixture(scope="session", autouse=True)
def _setup_db(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("db") / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    from app.config import settings
    settings.database_url = f"sqlite:///{db_path}"
    # Force re-create engine with new URL
    import importlib
    import app.db as db_mod
    importlib.reload(db_mod)
    import app.models  # noqa: F401
    db_mod.init_db()

    # Seed minimal users
    from app.auth import hash_password
    from app.models import Role, User
    s = db_mod.SessionLocal()
    try:
        s.add(User(email="admin@vbiz.vn", full_name="Admin",
                   password_hash=hash_password("admin123"), role=Role.admin))
        s.commit()
    finally:
        s.close()
    yield


@pytest.fixture
def client():
    # Import after env vars set
    import importlib
    import app.main as main_mod
    importlib.reload(main_mod)
    return TestClient(main_mod.app)


@pytest.fixture
def auth_client(client):
    client.post("/login", data={"email": "admin@vbiz.vn", "password": "admin123"},
                follow_redirects=False)
    return client
