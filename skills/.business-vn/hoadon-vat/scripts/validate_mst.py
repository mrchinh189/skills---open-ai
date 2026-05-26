"""Kiểm tra checksum mã số thuế Việt Nam (10 hoặc 13 chữ số).

Thuật toán: 9 chữ số đầu nhân lần lượt với hệ số [31,29,23,19,17,13,7,5,3],
tổng modulo 11, lấy 10 trừ kết quả = chữ số kiểm tra (chữ số thứ 10).
13 chữ số = MST chính (10 số) + dấu '-' + 3 chữ số đơn vị phụ thuộc.

Usage:
    python validate_mst.py 0123456789
    python validate_mst.py 0123456789-001
"""
from __future__ import annotations

import sys

WEIGHTS = [31, 29, 23, 19, 17, 13, 7, 5, 3]


def normalize(mst: str) -> str:
    return mst.replace("-", "").replace(" ", "").strip()


def is_valid_mst(mst: str) -> bool:
    code = normalize(mst)
    if len(code) not in (10, 13) or not code.isdigit():
        return False

    base = code[:10]
    total = sum(int(d) * w for d, w in zip(base[:9], WEIGHTS))
    check = (10 - total % 11) % 10
    return check == int(base[9])


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python validate_mst.py <mst>", file=sys.stderr)
        return 2
    mst = argv[1]
    ok = is_valid_mst(mst)
    print(f"{mst}: {'VALID' if ok else 'INVALID'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
