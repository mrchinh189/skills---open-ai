"""Seed dữ liệu mẫu cho VBiz Skills Platform.

Chạy: python -m scripts.seed
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.auth import hash_password
from app.db import SessionLocal, init_db
from app.models import (
    Customer,
    Document,
    Employee,
    LeadStatus,
    Product,
    Role,
    User,
)


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).first():
            print("DB đã có dữ liệu — bỏ qua seed.")
            return

        # Users
        db.add_all([
            User(email="admin@vbiz.vn", full_name="Quản trị viên", password_hash=hash_password("admin123"), role=Role.admin),
            User(email="manager@vbiz.vn", full_name="Nguyễn Quản Lý", password_hash=hash_password("manager123"), role=Role.manager),
            User(email="staff@vbiz.vn", full_name="Trần Nhân Viên", password_hash=hash_password("staff123"), role=Role.staff),
        ])

        # Customers
        db.add_all([
            Customer(name="Công ty CP FPT", tax_code="0101248141", phone="0901234567",
                     email="contact@fpt.com.vn", lead_status=LeadStatus.won, lead_score=95),
            Customer(name="Vinamilk", tax_code="0300588569", phone="0289123456",
                     email="info@vinamilk.com.vn", lead_status=LeadStatus.qualified, lead_score=75),
            Customer(name="Anh Nguyễn Văn A", phone="0987654321", lead_status=LeadStatus.new, lead_score=30),
            Customer(name="Khách lẻ tại quầy", lead_status=LeadStatus.contacted, lead_score=15),
        ])

        # Products
        db.add_all([
            Product(sku="SP001", name="Laptop Dell Latitude 5540", unit="chiếc",
                    price=Decimal("25000000"), vat_rate=Decimal("10"), stock=12),
            Product(sku="SP002", name="Chuột Logitech MX Master", unit="chiếc",
                    price=Decimal("2500000"), vat_rate=Decimal("10"), stock=50),
            Product(sku="SP003", name="Phần mềm kế toán MISA (1 năm)", unit="bản quyền",
                    price=Decimal("8000000"), vat_rate=Decimal("8"), stock=999),
            Product(sku="SP004", name="Dịch vụ tư vấn quản trị", unit="giờ",
                    price=Decimal("1500000"), vat_rate=Decimal("10"), stock=999),
        ])

        # Employees
        db.add_all([
            Employee(code="NV001", full_name="Lê Văn Bình", position="Trưởng phòng",
                     department="Kinh doanh", base_salary=Decimal("25000000"), dependents=2, joined_at=date(2021, 3, 15)),
            Employee(code="NV002", full_name="Phạm Thị Hoa", position="Kế toán trưởng",
                     department="Tài chính", base_salary=Decimal("20000000"), dependents=1, joined_at=date(2022, 6, 1)),
            Employee(code="NV003", full_name="Hoàng Văn Cường", position="Nhân viên IT",
                     department="Kỹ thuật", base_salary=Decimal("15000000"), dependents=0, joined_at=date(2023, 10, 20)),
        ])

        # Documents (cho RAG)
        db.add_all([
            Document(
                title="Chính sách nghỉ phép 2025",
                category="policy",
                content=(
                    "Mỗi nhân viên được nghỉ phép năm 12 ngày, cộng thêm 1 ngày cho mỗi 5 năm công tác. "
                    "Đơn xin nghỉ phải gửi trước ít nhất 3 ngày làm việc qua hệ thống VBiz. "
                    "Nghỉ ốm có giấy bác sĩ không tính vào phép năm."
                ),
            ),
            Document(
                title="Quy trình xuất hoá đơn VAT",
                category="sop",
                content=(
                    "Bước 1: Đơn hàng phải ở trạng thái 'confirmed' hoặc 'shipped'. "
                    "Bước 2: Vào trang Đơn hàng, click '→ Hoá đơn'. "
                    "Bước 3: Hệ thống tự sinh số hoá đơn liên tục theo ký hiệu 1C24TAA. "
                    "Bước 4: Kiểm tra MST khách hàng (10 hoặc 13 số) trước khi gửi. "
                    "Lưu ý: Thuế suất VAT 8% chỉ áp dụng theo nghị quyết Quốc hội từng giai đoạn."
                ),
            ),
            Document(
                title="Mức lương tối thiểu vùng 2024",
                category="policy",
                content=(
                    "Vùng I: 4,960,000 đ/tháng. Vùng II: 4,410,000 đ. Vùng III: 3,860,000 đ. Vùng IV: 3,450,000 đ. "
                    "Áp dụng từ 01/07/2024. Mức đóng BHTN tối đa = 20 lần lương tối thiểu vùng."
                ),
            ),
        ])

        db.commit()
        print("✅ Seed xong: 3 user, 4 khách hàng, 4 sản phẩm, 3 nhân viên, 3 tài liệu.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
