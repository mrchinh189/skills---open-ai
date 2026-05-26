---
name: cham-cong
description: Tính lương, chấm công, tăng ca, BHXH/BHYT/BHTN cho lao động Việt Nam theo Bộ luật Lao động 2019 và Luật BHXH. Dùng khi người dùng muốn tính lương net/gross, xử lý OT (150%/200%/300%), tính bảo hiểm bắt buộc, hoặc xuất bảng lương tháng.
metadata:
  short-description: Chấm công & tính lương theo luật Việt Nam
  language: vi
---

# Chấm Công & Lương (Việt Nam)

## Khi nào dùng

- Tính lương gross ↔ net
- Tính tiền tăng ca, làm đêm, làm ngày lễ
- Tính BHXH (8%), BHYT (1.5%), BHTN (1%) phần người lao động đóng
- Tính thuế TNCN luỹ tiến 7 bậc
- Xuất bảng lương / phiếu lương

## Hằng số (cập nhật 2024-2025)

| Khoản | Tỷ lệ NLĐ đóng | Trần |
|---|---|---|
| BHXH | 8% | 20× lương cơ sở |
| BHYT | 1.5% | 20× lương cơ sở |
| BHTN | 1% | 20× lương tối thiểu vùng |
| Lương tối thiểu vùng I | 4,960,000 đ/tháng | (từ 01/07/2024) |
| Giảm trừ bản thân | 11,000,000 đ/tháng | |
| Giảm trừ NPT | 4,400,000 đ/người/tháng | |

⚠️ **Luôn xác nhận** các con số trên trước khi xuất bảng lương — luật cập nhật thường xuyên.

## Hệ số tăng ca

| Loại | Hệ số |
|---|---|
| Ngày thường (giờ thứ 9 trở đi) | 150% |
| Ngày nghỉ tuần | 200% |
| Ngày lễ, Tết | 300% |
| Làm đêm (22h-6h) | +30% |

## Công thức tính lương net

```
Lương gộp = Lương cơ bản + Phụ cấp + Tiền OT
Bảo hiểm bắt buộc = Lương đóng BH × (8% + 1.5% + 1%)
Thu nhập tính thuế = Lương gộp − Bảo hiểm − Giảm trừ bản thân − Giảm trừ NPT − Khoản miễn thuế khác
Thuế TNCN = TNCN luỹ tiến 7 bậc trên Thu nhập tính thuế
Lương net = Lương gộp − Bảo hiểm − Thuế TNCN
```

## Bậc thuế TNCN

| Bậc | Thu nhập chịu thuế/tháng | Thuế suất |
|---|---|---|
| 1 | ≤ 5 triệu | 5% |
| 2 | > 5 → 10 triệu | 10% |
| 3 | > 10 → 18 triệu | 15% |
| 4 | > 18 → 32 triệu | 20% |
| 5 | > 32 → 52 triệu | 25% |
| 6 | > 52 → 80 triệu | 30% |
| 7 | > 80 triệu | 35% |

## Workflow

1. Nhập: lương cơ bản, ngày công thực tế, giờ OT (chia theo loại), số NPT, các phụ cấp.
2. Tính lương gộp.
3. Tính bảo hiểm (chú ý trần).
4. Tính thuế TNCN luỹ tiến.
5. Xuất phiếu lương: tổng/khấu trừ/thực nhận.

## Tránh

- KHÔNG dùng cho hợp đồng ngoài (cộng tác viên) — họ chịu thuế khoán 10%.
- KHÔNG quên cộng phụ cấp ăn ca miễn thuế (≤ 730k/tháng).
