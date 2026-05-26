# 🏢 VBiz Skills Platform

> Nền tảng quản trị doanh nghiệp Việt Nam tích hợp **Agent Skills** + **OpenAI** — kết hợp 4 trụ cột trong 1 codebase: **ERP/CRM + RAG Agent + Intranet + Skill catalog VN**.

Đây là ứng dụng tham chiếu cho repo [`skills---open-ai`](../). Nó vừa **sử dụng** các Agent Skill (đọc `SKILL.md` runtime), vừa **đóng góp** 5 skill VN mới dưới [`../skills/.business-vn/`](../skills/.business-vn/).

---

## ✨ Tính năng

| Module | Mô tả | Sử dụng skill |
|---|---|---|
| Auth + RBAC | Đăng nhập session, 3 vai trò (admin/manager/staff) | — |
| Khách hàng & Lead | CRUD + lead scoring BANT, kiểm tra MST checksum | `crm-lead`, `hoadon-vat` |
| Sản phẩm | Catalog + thuế suất VAT (0/5/8/10%) | `hoadon-vat` |
| Đơn hàng | Tạo đơn, tính VAT từng dòng, chuyển trạng thái | `hoadon-vat` |
| Hoá đơn VAT | Sinh số liên tục, in mẫu theo TT 78/2021 | `hoadon-vat` |
| Nhân sự + Lương | Tính lương net với BHXH/BHYT/BHTN + TNCN 7 bậc | `cham-cong` |
| Chấm công | Ghi nhận giờ làm + OT | `cham-cong` |
| Tài liệu nội bộ | KB + tìm kiếm, dùng làm nguồn RAG | — |
| 🤖 Agent RAG | Hỏi đáp dùng OpenAI (mock nếu không có key), tự chọn skill phù hợp, retrieve tài liệu nội bộ | tất cả 5 skill VN |

---

## 🚀 Chạy local trong 60 giây

```bash
cd business-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                  # (tuỳ chọn) điền OPENAI_API_KEY
python -m scripts.seed                # tạo DB + dữ liệu mẫu
PYTHONPATH=. uvicorn app.main:app --reload
```

Mở http://localhost:8000 → đăng nhập với `admin@vbiz.vn` / `admin123`.

### Hoặc Docker

```bash
cd business-app
docker compose up --build
```

---

## 🧪 Test

```bash
cd business-app
PYTHONPATH=. pytest -q
```

CI sẽ tự chạy với mỗi PR (xem `.github/workflows/ci.yml`).

---

## 🗂 Cấu trúc

```
business-app/
├── app/
│   ├── main.py             ← FastAPI entrypoint
│   ├── config.py           ← Pydantic settings
│   ├── db.py + models.py   ← SQLAlchemy 2.x
│   ├── auth.py             ← session + RBAC
│   ├── finance.py          ← MST checksum, VAT, lương VN, lead scoring
│   ├── ai.py               ← Loader skill + OpenAI client (mock fallback)
│   ├── routers/            ← 9 router (auth, home, customers, products,
│   │                          orders, invoices, employees, attendance,
│   │                          documents, agent)
│   ├── templates/          ← Jinja2 + Tailwind CDN + HTMX
│   └── static/
├── scripts/seed.py
├── tests/                  ← pytest (finance + endpoints + skill script)
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── requirements.txt
```

---

## 🧩 5 Agent Skill VN đi kèm

Dưới `../skills/.business-vn/` — theo đúng chuẩn `SKILL.md` của repo gốc:

1. **hoadon-vat** — Hoá đơn VAT theo TT 78/2021, có script `validate_mst.py` kiểm tra checksum MST.
2. **cham-cong** — Tính lương + BHXH/BHYT/BHTN + TNCN luỹ tiến 7 bậc.
3. **crm-lead** — Quản lý pipeline lead với BANT scoring, mẫu email VN.
4. **baocao-tai-chinh** — Lập 4 BCTC theo TT 200/TT 133.
5. **hop-dong** — Soạn & rà soát hợp đồng theo BLDS 2015 + LTM 2005, checklist 10 điểm rủi ro.

Agent tại `/agent` sẽ **tự đọc các SKILL.md này** lúc runtime và chọn skill phù hợp với câu hỏi.

---

## 🔐 Tài khoản demo

| Email | Mật khẩu | Vai trò |
|---|---|---|
| `admin@vbiz.vn` | `admin123` | admin |
| `manager@vbiz.vn` | `manager123` | manager |
| `staff@vbiz.vn` | `staff123` | staff |

---

## ⚠️ Lưu ý sản xuất

Trước khi triển khai thực:

- [ ] Đổi `SECRET_KEY` và toàn bộ mật khẩu mặc định.
- [ ] Chuyển `DATABASE_URL` sang PostgreSQL.
- [ ] Bật HTTPS (reverse proxy: Caddy / Nginx).
- [ ] Tích hợp chữ ký số thật cho hoá đơn (hiện chỉ là mẫu hiển thị).
- [ ] Kiểm tra lại các hằng số luật (lương tối thiểu, thuế suất 8%) — luật cập nhật thường xuyên.
- [ ] Thêm rate limit cho endpoint `/agent` để tránh đốt token OpenAI.

---

## 📜 License

MIT — xem `LICENSE.txt` trong từng skill và `pyproject.toml`.
