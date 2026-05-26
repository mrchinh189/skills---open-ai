"""Toán tài chính Việt Nam: VAT, lương, MST."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

WEIGHTS = [31, 29, 23, 19, 17, 13, 7, 5, 3]


def is_valid_mst(mst: str) -> bool:
    code = mst.replace("-", "").replace(" ", "").strip()
    if len(code) not in (10, 13) or not code.isdigit():
        return False
    base = code[:10]
    total = sum(int(d) * w for d, w in zip(base[:9], WEIGHTS))
    check = (10 - total % 11) % 10
    return check == int(base[9])


def compute_vat(subtotal: Decimal, rate: Decimal) -> Decimal:
    return (subtotal * rate / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# Bậc thuế TNCN luỹ tiến (tháng): (đến_mức, thuế_suất, khấu_trừ_nhanh)
PIT_BRACKETS = [
    (Decimal("5000000"), Decimal("0.05"), Decimal("0")),
    (Decimal("10000000"), Decimal("0.10"), Decimal("250000")),
    (Decimal("18000000"), Decimal("0.15"), Decimal("750000")),
    (Decimal("32000000"), Decimal("0.20"), Decimal("1650000")),
    (Decimal("52000000"), Decimal("0.25"), Decimal("3250000")),
    (Decimal("80000000"), Decimal("0.30"), Decimal("5850000")),
    (Decimal("9" * 18), Decimal("0.35"), Decimal("9850000")),
]

SELF_DEDUCTION = Decimal("11000000")
DEPENDENT_DEDUCTION = Decimal("4400000")
SI_RATE = Decimal("0.105")  # BHXH 8% + BHYT 1.5% + BHTN 1%


def compute_pit(taxable: Decimal) -> Decimal:
    if taxable <= 0:
        return Decimal("0")
    for ceiling, rate, quick in PIT_BRACKETS:
        if taxable <= ceiling:
            return (taxable * rate - quick).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal("0")


def compute_payroll(
    base_salary: Decimal,
    days_worked: Decimal,
    standard_days: Decimal = Decimal("22"),
    ot_normal_hours: Decimal = Decimal("0"),
    ot_weekend_hours: Decimal = Decimal("0"),
    ot_holiday_hours: Decimal = Decimal("0"),
    dependents: int = 0,
    allowance: Decimal = Decimal("0"),
) -> dict[str, Decimal]:
    daily = base_salary / standard_days if standard_days else Decimal("0")
    hourly = daily / Decimal("8")
    earned = daily * days_worked
    ot_pay = (
        ot_normal_hours * hourly * Decimal("1.5")
        + ot_weekend_hours * hourly * Decimal("2")
        + ot_holiday_hours * hourly * Decimal("3")
    )
    gross = earned + ot_pay + allowance
    social_insurance = (base_salary * SI_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    deduction = SELF_DEDUCTION + DEPENDENT_DEDUCTION * dependents
    taxable = gross - social_insurance - deduction
    pit = compute_pit(taxable)
    net = gross - social_insurance - pit
    return {
        "gross": gross.quantize(Decimal("0.01")),
        "social_insurance": social_insurance,
        "taxable": max(taxable, Decimal("0")).quantize(Decimal("0.01")),
        "pit": pit,
        "net": net.quantize(Decimal("0.01")),
    }


# Lead scoring
SCORE_CRITERIA = {
    "has_budget": 25,
    "decision_maker": 20,
    "urgent_need": 20,
    "size_match": 15,
    "uses_similar": 10,
    "referral": 10,
}


def lead_score(flags: dict[str, bool]) -> int:
    return sum(weight for key, weight in SCORE_CRITERIA.items() if flags.get(key))
