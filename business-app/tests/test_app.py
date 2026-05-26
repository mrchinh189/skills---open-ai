def test_health(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.text == "ok"


def test_login_required(client):
    # / redirect tới /login khi chưa đăng nhập
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (303, 307)


def test_login_flow(client):
    r = client.post(
        "/login",
        data={"email": "admin@vbiz.vn", "password": "admin123"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers["location"] == "/"


def test_dashboard_after_login(auth_client):
    r = auth_client.get("/")
    assert r.status_code == 200
    assert "Dashboard" in r.text


def test_customers_page(auth_client):
    r = auth_client.get("/customers")
    assert r.status_code == 200


def test_create_customer_validates_mst(auth_client):
    r = auth_client.post(
        "/customers/new",
        data={"name": "Cty X", "tax_code": "9999999999"},  # checksum sai
        follow_redirects=False,
    )
    # Form trả về 400 + render lại form với error
    assert r.status_code == 400
    assert "không hợp lệ" in r.text


def test_agent_loads_skills(auth_client):
    r = auth_client.get("/agent")
    assert r.status_code == 200
    # 5 skill .business-vn nên xuất hiện trong sidebar
    assert "hoadon-vat" in r.text or "cham-cong" in r.text


def test_agent_chat_mock_mode(auth_client):
    r = auth_client.post("/agent", data={"query": "Tính lương net 20 triệu"})
    assert r.status_code == 200
    # Khi không có API key → mode mock
    assert "mock" in r.text.lower() or "openai" in r.text.lower()
