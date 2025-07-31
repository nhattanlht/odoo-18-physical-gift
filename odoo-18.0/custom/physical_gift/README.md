# Physical Gift Module

## Mô tả
Module Physical Gift được thiết kế để quản lý các chương trình quà tặng vật lý trong Odoo. Module này cung cấp giao diện quản lý tương tự như hình ảnh đính kèm với các tính năng:

- Quản lý danh sách chương trình quà tặng
- Tìm kiếm và lọc chương trình theo tên
- Xuất dữ liệu ra file CSV
- Thêm và cập nhật chương trình
- Quản lý trạng thái chương trình (Nháp, Hoạt động, Không hoạt động, Đã đóng)

## Cài đặt

1. Copy module vào thư mục `custom/` của Odoo
2. Cập nhật danh sách ứng dụng trong Odoo
3. Cài đặt module "Physical Gift"
4. Cấp quyền cho người dùng cần thiết

## Cấu trúc Module

```
physical_gift/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── physical_gift_program.py
├── views/
│   ├── physical_gift_views.xml
│   └── physical_gift_menus.xml
├── security/
│   ├── physical_gift_security.xml
│   └── ir.model.access.csv
├── data/
│   ├── physical_gift_data.xml
│   └── physical_gift_demo.xml
├── static/
│   ├── src/
│   │   ├── css/
│   │   │   └── physical_gift.css
│   │   └── js/
│   │       └── physical_gift.js
│   └── description/
└── README.md
```

## Tính năng chính

### 1. Quản lý chương trình
- Tạo, chỉnh sửa, xóa chương trình quà tặng
- Quản lý thông tin: tên, công ty, người tạo, ngày bắt đầu/kết thúc
- Theo dõi trạng thái chương trình

### 2. Quản lý quà tặng
- Thêm quà tặng vào chương trình
- Quản lý số lượng và đơn giá
- Tính toán tổng giá trị

### 3. Tìm kiếm và lọc
- Tìm kiếm theo tên chương trình
- Lọc theo công ty, người tạo, trạng thái
- Nhóm theo các tiêu chí khác nhau

### 4. Xuất dữ liệu
- Xuất danh sách chương trình ra file CSV
- Bao gồm thông tin: ID, tên, công ty, người tạo, trạng thái

## Quyền truy cập

Module có 2 nhóm quyền:
- **Physical Gift User**: Có thể đọc, tạo, chỉnh sửa nhưng không xóa
- **Physical Gift Manager**: Có đầy đủ quyền bao gồm xóa

## Sử dụng

1. Vào menu "Physical Gift" > "Chương trình" > "Quản lý chương trình"
2. Sử dụng các nút "Lọc", "Reset", "Xuất file", "Thêm chương trình"
3. Click vào nút "Cập nhật" để chỉnh sửa chương trình
4. Quản lý trạng thái chương trình bằng các nút trong form

## Demo Data

Module bao gồm dữ liệu demo với các chương trình mẫu:
- Vietinbank (Client Integration)
- HN's Loyalty (Integration)
- Chương trình SC-Bank (Got It)
- AIA Vietnam Program (AIA Vietnam)

## Tùy chỉnh

### CSS
File `static/src/css/physical_gift.css` chứa các style tùy chỉnh cho giao diện.

### JavaScript
File `static/src/js/physical_gift.js` chứa logic tùy chỉnh cho các tính năng như xuất file, lọc dữ liệu.

## Hỗ trợ

Để báo cáo lỗi hoặc yêu cầu tính năng mới, vui lòng liên hệ team phát triển. 