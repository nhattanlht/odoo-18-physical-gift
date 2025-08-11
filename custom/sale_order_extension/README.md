# Sale Order Extension Module

## Mô tả
Module này mở rộng chức năng của Sale Order trong Odoo bằng cách thêm các trường thông tin bổ sung và cải thiện giao diện người dùng.

## Tính năng chính

### 1. Thông tin PO (Purchase Order)
- **PO Path**: Đường dẫn đến tài liệu Purchase Order
- **PO Number**: Số Purchase Order

### 2. Phân loại đơn hàng
- **Loại đơn hàng**: Standard, Express, Bulk Order, Custom
- **Trạng thái đơn hàng**: Draft, Confirmed, In Progress, Shipped, Delivered, Cancelled
- **Print Legal**: Dayone, Davone (mặc định), Other

### 3. Thông tin giao hàng
- **Địa chỉ giao hàng**: Địa chỉ đầy đủ
- **Delivery Code**: Mã định danh giao hàng
- **Thông tin người nhận**: 3 trường thông tin người nhận
- **Ghi chú nhận hàng**: Ghi chú đặc biệt cho việc giao/nhận hàng

### 4. Ghi chú chung
- **Ghi chú**: Ghi chú tổng quát cho đơn hàng

## Cài đặt

1. Copy module vào thư mục `custom/`
2. Cập nhật danh sách ứng dụng trong Odoo
3. Cài đặt module "Sale Order Extension"
4. Khởi động lại Odoo server

## Sử dụng

Sau khi cài đặt, khi tạo hoặc chỉnh sửa Sale Order, bạn sẽ thấy:
- Tab mới "PO Information" chứa thông tin PO và phân loại đơn hàng
- Tab mới "Delivery Information" chứa thông tin giao hàng và người nhận
- Các trường được tổ chức theo nhóm logic
- Giá trị mặc định cho Print Legal là "Davone"

## Yêu cầu hệ thống
- Odoo 18.0
- Module Sale đã được cài đặt

## Tác giả
Module được phát triển để mở rộng chức năng Sale Order theo yêu cầu cụ thể. 