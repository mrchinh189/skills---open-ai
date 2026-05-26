---
name: baocao-tai-chinh
description: Lập báo cáo tài chính theo Thông tư 200/2014/TT-BTC (doanh nghiệp lớn) hoặc Thông tư 133/2016/TT-BTC (doanh nghiệp nhỏ và vừa) tại Việt Nam. Dùng khi cần lập Bảng cân đối kế toán, Báo cáo KQKD, Báo cáo lưu chuyển tiền tệ, hoặc thuyết minh BCTC.
metadata:
  short-description: Báo cáo tài chính TT200 / TT133
  language: vi
---

# Báo Cáo Tài Chính (Việt Nam)

## Khi nào dùng

- Lập 4 BCTC bắt buộc: BCĐKT, BC KQKD, BC LCTT, Thuyết minh
- Đối chiếu số dư đầu kỳ / cuối kỳ
- Phân loại tài khoản theo hệ thống TKKT VN

## Hai khung kế toán

| | TT200/2014 | TT133/2016 |
|---|---|---|
| Đối tượng | Doanh nghiệp lớn | DN nhỏ & vừa (≤200 LĐ, DT ≤200 tỷ) |
| Số TK | 81 tài khoản cấp 1 | Đơn giản hơn |
| Hợp nhất | Bắt buộc nếu có công ty con | Tuỳ chọn |

## Phương trình kế toán

```
TÀI SẢN = NỢ PHẢI TRẢ + VỐN CHỦ SỞ HỮU
```

Phải LUÔN khớp tới đồng. Nếu lệch → sai dữ liệu đầu vào, không tự "ép" bằng tài khoản khác.

## Cấu trúc BCĐKT (rút gọn)

```
TÀI SẢN
├── A. Tài sản ngắn hạn (Mã 100)
│   ├── I. Tiền và tương đương tiền (110)
│   ├── II. Đầu tư TC ngắn hạn (120)
│   ├── III. Phải thu ngắn hạn (130)
│   ├── IV. Hàng tồn kho (140)
│   └── V. TS ngắn hạn khác (150)
└── B. Tài sản dài hạn (Mã 200)
    ├── I. Phải thu dài hạn (210)
    ├── II. TSCĐ (220)
    ├── III. Bất động sản đầu tư (230)
    ├── IV. Đầu tư TC dài hạn (250)
    └── V. TS dài hạn khác (260)

NGUỒN VỐN
├── C. Nợ phải trả (300)
│   ├── I. Nợ ngắn hạn (310)
│   └── II. Nợ dài hạn (330)
└── D. Vốn chủ sở hữu (400)
    ├── I. Vốn chủ sở hữu (410)
    └── II. Nguồn kinh phí (430)
```

## Báo cáo KQKD (cốt lõi)

```
Doanh thu thuần (10) = DT bán hàng (01) − Các khoản giảm trừ (02)
Lợi nhuận gộp (20) = (10) − Giá vốn (11)
LN thuần từ HĐKD (30) = (20) + DT tài chính − CP TC − CP bán hàng − CP QLDN
LN trước thuế (50) = (30) + LN khác (40)
LN sau thuế (60) = (50) − CP thuế TNDN (51,52)
```

## Workflow

1. Kết chuyển: doanh thu, chi phí → 911 → 421 (tự động cuối kỳ).
2. Lập BCĐKT theo mã chỉ tiêu — kiểm tra TS = NPT + VCSH.
3. Lập BC KQKD — kiểm tra LN sau thuế khớp với 421.
4. Lập LCTT (gián tiếp): bắt đầu từ LN trước thuế, điều chỉnh khấu hao, biến động vốn lưu động.
5. Thuyết minh: chính sách kế toán, chi tiết các khoản trọng yếu.

## Tránh

- KHÔNG bỏ qua bút toán điều chỉnh cuối kỳ (khấu hao, dự phòng).
- KHÔNG làm tròn quá đáng — sai số tích luỹ sẽ gây lệch BCĐKT.
- KHÔNG xuất BCTC chưa có chữ ký của KTT và GĐ.
