---
name: crm-lead
description: Quản lý khách hàng tiềm năng (lead) và pipeline bán hàng cho doanh nghiệp B2B/B2C Việt Nam. Dùng khi cần phân loại lead theo BANT, chấm điểm (lead scoring), chuyển trạng thái pipeline (New → Qualified → Proposal → Won/Lost), hoặc soạn email/zalo follow-up bằng tiếng Việt.
metadata:
  short-description: Lead pipeline & follow-up (Việt Nam)
  language: vi
---

# CRM Lead Management

## Khi nào dùng

- Phân loại lead mới (BANT: Budget / Authority / Need / Timeline)
- Chấm điểm lead (0-100)
- Soạn email / tin nhắn Zalo OA follow-up
- Đề xuất next action

## Trạng thái pipeline chuẩn

```
NEW ──► CONTACTED ──► QUALIFIED ──► PROPOSAL ──► NEGOTIATION ──┬─► WON
                          │                                     │
                          └──► DISQUALIFIED                     └─► LOST
```

## Lead scoring (mặc định)

| Tiêu chí | Điểm |
|---|---|
| Có ngân sách rõ ràng | +25 |
| Người quyết định trực tiếp | +20 |
| Nhu cầu cấp thiết (< 30 ngày) | +20 |
| Quy mô khớp (SMB/Enterprise) | +15 |
| Đã dùng giải pháp tương tự | +10 |
| Đến từ giới thiệu (referral) | +10 |
| Total ≥ 70 → Qualified | |

## Mẫu email follow-up (VN)

```
Chủ đề: {Tên công ty} - Theo dõi nhu cầu {giải pháp}

Kính gửi anh/chị {Họ tên},

Cảm ơn anh/chị đã dành thời gian trao đổi với {Tên công ty bạn} ngày {ngày}.
Theo nội dung trao đổi, em xin tóm tắt nhu cầu của anh/chị như sau:
- {nhu cầu 1}
- {nhu cầu 2}

Em đính kèm đề xuất sơ bộ {file}. Anh/chị xem qua giúp em và phản hồi
trước {deadline} nhé.

Trân trọng,
{Tên SDR}
{SĐT} | {Email}
```

## Tránh

- KHÔNG thúc giục lead < 24h sau lần đầu liên hệ.
- KHÔNG dùng "Dear Mr/Ms" cho khách Việt — dùng "Kính gửi anh/chị".
- KHÔNG chuyển sang WON khi chưa có hợp đồng ký số/giấy.

## Workflow đề xuất

1. Lead vào → tự động NEW.
2. Trong 4h: gọi/zalo đầu tiên → CONTACTED.
3. Trong 48h: chấm BANT → QUALIFIED hoặc DISQUALIFIED.
4. Trong 7 ngày: gửi proposal → PROPOSAL.
5. Negotiation tối đa 14 ngày → WON/LOST.
6. Lead LOST: re-engage sau 90 ngày.
