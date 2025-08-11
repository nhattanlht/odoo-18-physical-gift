# Physical Gift API - Quick Start

## Cài đặt và Sử dụng

### 1. Cài đặt Module
```bash
# Copy module vào thư mục addons của Odoo
# Hoặc sử dụng custom addons path
```

### 2. Cập nhật Module
- Vào Odoo > Apps > Update Apps List
- Tìm "Physical Gift Management" và cài đặt/cập nhật

### 3. Test API
```bash
# Chạy test script
cd custom/physical_gift
python test_api.py
```

## API Endpoints Chính

### Brands (Thương hiệu)
- `GET /api/physical-gift/brands` - Lấy danh sách thương hiệu
- `GET /api/physical-gift/brands/{id}` - Lấy chi tiết thương hiệu

### Categories (Danh mục)
- `GET /api/physical-gift/categories` - Lấy danh sách danh mục

### Items (Sản phẩm)
- `GET /api/physical-gift/items` - Lấy danh sách sản phẩm
- `GET /api/physical-gift/items?brand_id=1` - Filter theo thương hiệu

### Programs (Chương trình)
- `GET /api/physical-gift/programs` - Lấy danh sách chương trình

### Orders (Đơn hàng)
- `GET /api/physical-gift/orders` - Lấy danh sách đơn hàng
- `POST /api/physical-gift/orders` - Tạo đơn hàng mới
- `PUT /api/physical-gift/orders/{id}` - Cập nhật đơn hàng

### Suppliers (Nhà cung cấp)
- `GET /api/physical-gift/suppliers` - Lấy danh sách nhà cung cấp

### Shipping Units (Đơn vị vận chuyển)
- `GET /api/physical-gift/shipping-units` - Lấy danh sách đơn vị vận chuyển

## Ví dụ Sử dụng

### JavaScript
```javascript
// Lấy danh sách thương hiệu
fetch('/api/physical-gift/brands')
  .then(response => response.json())
  .then(data => console.log(data));

// Tạo đơn hàng
fetch('/api/physical-gift/orders', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    program_id: 1,
    recipient_name: 'Nguyễn Văn A',
    recipient_phone: '0123456789',
    total_order_value: 1500000
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL
```bash
# Lấy danh sách thương hiệu
curl -X GET "http://localhost:8069/api/physical-gift/brands"

# Tạo đơn hàng
curl -X POST "http://localhost:8069/api/physical-gift/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "program_id": 1,
    "recipient_name": "Nguyễn Văn A",
    "recipient_phone": "0123456789",
    "total_order_value": 1500000
  }'
```

## Lưu ý

1. **Authentication**: API hiện tại cho phép truy cập công khai. Cần implement authentication cho production.

2. **Base URL**: Thay đổi `localhost:8069` thành domain thực tế của bạn.

3. **Error Handling**: Tất cả response đều có format:
   ```json
   {
     "success": true/false,
     "data": [...],
     "error": "message" // nếu có lỗi
   }
   ```

4. **Documentation**: Xem file `API_DOCUMENTATION.md` để biết chi tiết đầy đủ.

## Troubleshooting

1. **Module không load**: Kiểm tra log Odoo và đảm bảo module được cài đặt đúng cách.

2. **API không hoạt động**: Kiểm tra Odoo server đang chạy và port đúng.

3. **Permission denied**: Đảm bảo user có quyền truy cập các model tương ứng.

4. **Data không hiển thị**: Kiểm tra có dữ liệu trong database và các record có `active=True`. 