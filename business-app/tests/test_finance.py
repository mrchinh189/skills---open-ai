from decimal import Decimal

from app.finance import (
    SCORE_CRITERIA,
    compute_payroll,
    compute_pit,
    compute_vat,
    is_valid_mst,
    lead_score,
)


def test_mst_valid_checksum():
    # 0101248141 = MST FPT thực tế, hợp lệ
    assert is_valid_mst("0101248141")


def test_mst_invalid_length():
    assert not is_valid_mst("12345")
    assert not is_valid_mst("12345678")


def test_mst_invalid_checksum():
    assert not is_valid_mst("0101248140")  # đổi chữ số cuối


def test_mst_with_branch_suffix():
    # 13 chữ số = MST chính + chi nhánh
    assert is_valid_mst("0101248141-001")


def test_vat_basic():
    assert compute_vat(Decimal("1000000"), Decimal("10")) == Decimal("100000.00")
    assert compute_vat(Decimal("500000"), Decimal("8")) == Decimal("40000.00")


def test_pit_progressive():
    # 5tr → bậc 1: 5% = 250k
    assert compute_pit(Decimal("5000000")) == Decimal("250000.00")
    # 8tr → 5%*5tr + 10%*3tr = 250+300 = 550k → 8tr*10% - 250k = 550k
    assert compute_pit(Decimal("8000000")) == Decimal("550000.00")


def test_payroll_smoke():
    r = compute_payroll(
        base_salary=Decimal("20000000"),
        days_worked=Decimal("22"),
        dependents=1,
    )
    assert r["gross"] > 0
    assert r["net"] > 0
    assert r["net"] < r["gross"]


def test_lead_score_threshold():
    assert lead_score({k: True for k in SCORE_CRITERIA}) == sum(SCORE_CRITERIA.values())
    assert lead_score({"has_budget": True, "decision_maker": True}) == 45
    assert lead_score({}) == 0
