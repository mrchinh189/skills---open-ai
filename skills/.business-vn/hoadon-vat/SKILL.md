---
name: hoadon-vat
description: Soạn và kiểm tra hoá đơn giá trị gia tăng (VAT) theo Thông tư 78/2021/TT-BTC và Nghị định 123/2020/NĐ-CP của Việt Nam. Dùng skill này khi người dùng muốn tạo hoá đơn điện tử, tính thuế VAT (0%, 5%, 8%, 10%), kiểm tra MST (mã số thuế), hoặc xuất file XML/PDF hoá đơn cho khách hàng doanh nghiệp Việt Nam.
metadata:
  short-description: Tạo & kiểm tra hoá đơn VAT (Việt Nam)
  language: vi
---

# Hoá Đơn VAT (Việt Nam)

## Khi nào dùng

Kích hoạt khi người dùng:
- Yêu cầu "lập hoá đơn", "xuất hoá đơn", "hoá đơn điện tử"
- Hỏi về thuế suất VAT, mã số thuế, ký hiệu hoá đơn
- Cần xuất XML hoá đơn điện tử theo chuẩn của Tổng cục Thuế
- Đối soát hoá đơn đầu vào / đầu ra

## Quy tắc cốt lõi

1. **Mã số thuế (MST):** 10 hoặc 13 chữ số. 13 chữ số = đơn vị phụ thuộc (suffix `-XXX`).
2. **Thuế suất VAT hiện hành:**
   - 0% — hàng xuất khẩu, vận tải quốc tế
   - 5% — nước sạch, sách giáo khoa, dịch vụ y tế (một phần)
   - 8% — áp dụng tạm thời theo NQ 142/2024/QH15 (gia hạn từng giai đoạn — luôn xác nhận hiệu lực)
   - 10% — mặc định
3. **Ký hiệu hoá đơn:** 1 ký tự + 6 ký tự (vd `1C24TAA`). Mẫu ký hiệu phải đăng ký với CQT.
4. **Số hoá đơn:** liên tục, không nhảy số, reset theo năm tài chính.
5. **Định dạng tiền:** VND không dấu phẩy thập phân khi xuất XML, dấu chấm phân tách hàng nghìn khi hiển thị.

## Workflow

1. **Thu thập thông tin tối thiểu:**
   - Bên bán: MST, tên, địa chỉ, số TK ngân hàng
   - Bên mua: MST (nếu có), tên, địa chỉ
   - Danh mục hàng/dịch vụ: tên, ĐVT, số lượng, đơn giá, thuế suất
   - Hình thức thanh toán: TM/CK/TM-CK

2. **Tính toán:**
   ```
   Thành tiền (i) = số_lượng(i) × đơn_giá(i)
   Cộng tiền hàng = Σ Thành tiền (i)
   Tiền thuế (theo từng nhóm thuế suất) = thành_tiền_nhóm × thuế_suất
   Tổng tiền thanh toán = Cộng tiền hàng + Σ Tiền thuế
   ```

3. **Xuất output:** XML theo chuẩn `Hóa đơn 1.1.0` của TCT, hoặc PDF hiển thị.

4. **Kiểm tra trước khi gửi:**
   - Tổng cộng = số bằng chữ (dùng helper `so_thanh_chu`)
   - MST hợp lệ (checksum modulo)
   - Ngày lập ≤ ngày hiện tại
   - Không có dòng nào số lượng âm

## Helper script

Xem `scripts/validate_mst.py` để kiểm tra checksum MST 10 số (thuật toán nhân hệ số 31,29,23,19,17,13,7,5,3 rồi modulo 11).

## Tránh

- KHÔNG tự ý hardcode thuế suất 8% — luôn kiểm tra văn bản hiện hành.
- KHÔNG gửi hoá đơn ra ngoài khi chưa có chữ ký số.
- KHÔNG dùng skill này để tư vấn pháp lý — chỉ hỗ trợ kỹ thuật.
