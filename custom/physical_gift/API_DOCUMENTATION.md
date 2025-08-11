# Physical Gift API Documentation

## Tổng quan
API này cung cấp các endpoint để tương tác với module Physical Gift Management trong Odoo.

## Base URL
```
http://your-odoo-domain.com
```

## Authentication
Hiện tại API sử dụng `auth='public'` và `csrf=False` để cho phép truy cập công khai. Trong môi trường production, bạn nên implement authentication phù hợp.

## Endpoints

### 1. Brands (Thương hiệu)

#### GET /api/physical-gift/brands
Lấy danh sách tất cả thương hiệu đang hoạt động.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Nike",
      "name_en": "Nike",
      "code": "NIKE",
      "website": "https://nike.com",
      "contact_person": "John Doe",
      "phone": "0123456789",
      "email": "contact@nike.com",
      "address": "123 Main St",
      "partnership_date": "2024-01-01",
      "contract_number": "CONTRACT001",
      "commission_rate": 10.0,
      "state": "active",
      "store_count": 5,
      "program_count": 3
    }
  ],
  "total": 1
}
```

#### GET /api/physical-gift/brands/{brand_id}
Lấy chi tiết thương hiệu theo ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Nike",
    "name_en": "Nike",
    "code": "NIKE",
    "website": "https://nike.com",
    "contact_person": "John Doe",
    "phone": "0123456789",
    "email": "contact@nike.com",
    "address": "123 Main St",
    "partnership_date": "2024-01-01",
    "contract_number": "CONTRACT001",
    "commission_rate": 10.0,
    "state": "active",
    "store_count": 5,
    "program_count": 3,
    "stores": [
      {
        "id": 1,
        "name": "Nike Store 1",
        "address": "456 Store St",
        "phone": "0987654321",
        "state": "active"
      }
    ],
    "programs": [
      {
        "id": 1,
        "name_vi": "Chương trình Nike 2024",
        "name_en": "Nike Program 2024",
        "state": "active"
      }
    ]
  }
}
```

### 2. Categories (Danh mục)

#### GET /api/physical-gift/categories
Lấy danh sách tất cả danh mục đang hoạt động.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Thể thao",
      "name_en": "Sports",
      "code": "SPORTS",
      "description": "Danh mục thể thao",
      "description_en": "Sports category",
      "parent_id": null,
      "parent_name": null,
      "sequence": 10,
      "item_count": 15,
      "program_count": 2
    }
  ],
  "total": 1
}
```

### 3. Items (Sản phẩm)

#### GET /api/physical-gift/items
Lấy danh sách sản phẩm với các filter tùy chọn.

**Query Parameters:**
- `brand_id`: ID thương hiệu
- `category_id`: ID danh mục
- `supplier_id`: ID nhà cung cấp

**Example:** `GET /api/physical-gift/items?brand_id=1&category_id=2`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Giày Nike Air Max",
      "brand_id": 1,
      "brand_name": "Nike",
      "category_id": 1,
      "category_name": "Thể thao",
      "supplier_id": 1,
      "supplier_name": "Nike Supplier",
      "quantity": 100,
      "unit_price": 1500000,
      "total_price": 150000000
    }
  ],
  "total": 1
}
```

### 4. Programs (Chương trình)

#### GET /api/physical-gift/programs
Lấy danh sách chương trình với các filter tùy chọn.

**Query Parameters:**
- `brand_redeem_id`: ID thương hiệu redeem
- `state`: Trạng thái chương trình

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name_vi": "Chương trình Nike 2024",
      "name_en": "Nike Program 2024",
      "name": "Chương trình Nike 2024",
      "brand_redeem_id": 1,
      "brand_redeem_name": "Nike",
      "store_redeem_id": 1,
      "store_redeem_name": "Nike Store 1",
      "bill_number": "BILL001",
      "state": "active",
      "company_id": 1,
      "company_name": "Your Company"
    }
  ],
  "total": 1
}
```

### 5. Orders (Đơn hàng)

#### GET /api/physical-gift/orders
Lấy danh sách đơn hàng với các filter tùy chọn.

**Query Parameters:**
- `program_id`: ID chương trình
- `order_status`: Trạng thái đơn hàng
- `payment_status`: Trạng thái thanh toán

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "ORDER001",
      "program_id": 1,
      "program_name": "Chương trình Nike 2024",
      "recipient_name": "Nguyễn Văn A",
      "recipient_phone": "0123456789",
      "total_order_value": 1500000,
      "voucher_code": "VOUCHER001",
      "shipping_unit_id": 1,
      "shipping_unit_name": "Giao hàng nhanh",
      "waybill_code": "WAYBILL001",
      "payment_gateway": "bank_transfer",
      "payment_status": "paid",
      "transaction_code": "TXN001",
      "product_type": "physical",
      "order_time": "2024-01-15 10:30:00",
      "create_date": "2024-01-15 10:30:00",
      "order_status": "confirmed",
      "error_content": null
    }
  ],
  "total": 1
}
```

#### POST /api/physical-gift/orders
Tạo đơn hàng mới.

**Required Fields:**
- `program_id`: ID chương trình
- `recipient_name`: Tên người nhận
- `recipient_phone`: Số điện thoại người nhận
- `total_order_value`: Tổng giá trị đơn hàng

**Optional Fields:**
- `voucher_code`: Mã voucher
- `shipping_unit_id`: ID đơn vị vận chuyển
- `waybill_code`: Mã vận đơn
- `payment_gateway`: Cổng thanh toán
- `payment_status`: Trạng thái thanh toán
- `transaction_code`: Mã giao dịch
- `product_type`: Loại sản phẩm
- `order_time`: Thời gian đặt hàng
- `order_status`: Trạng thái đơn hàng
- `error_content`: Nội dung lỗi

**Request Body:**
```json
{
  "program_id": 1,
  "recipient_name": "Nguyễn Văn A",
  "recipient_phone": "0123456789",
  "total_order_value": 1500000,
  "voucher_code": "VOUCHER001",
  "payment_gateway": "bank_transfer",
  "product_type": "physical"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "ORDER001",
    "message": "Order created successfully"
  }
}
```

#### PUT /api/physical-gift/orders/{order_id}
Cập nhật đơn hàng.

**Allowed Fields:**
- `recipient_name`
- `recipient_phone`
- `total_order_value`
- `voucher_code`
- `shipping_unit_id`
- `waybill_code`
- `payment_gateway`
- `payment_status`
- `transaction_code`
- `product_type`
- `order_status`
- `error_content`

**Request Body:**
```json
{
  "order_status": "confirmed",
  "payment_status": "paid",
  "waybill_code": "WAYBILL001"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "ORDER001",
    "message": "Order updated successfully"
  }
}
```

### 6. Suppliers (Nhà cung cấp)

#### GET /api/physical-gift/suppliers
Lấy danh sách nhà cung cấp đang hoạt động.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Nike Supplier",
      "code": "NIKE_SUP",
      "contact_person": "John Doe",
      "phone": "0123456789",
      "email": "contact@nike-supplier.com",
      "address": "123 Supplier St",
      "website": "https://nike-supplier.com",
      "state": "active"
    }
  ],
  "total": 1
}
```

### 7. Shipping Units (Đơn vị vận chuyển)

#### GET /api/physical-gift/shipping-units
Lấy danh sách đơn vị vận chuyển đang hoạt động.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Giao hàng nhanh",
      "code": "FAST_DELIVERY",
      "contact_person": "Jane Smith",
      "phone": "0987654321",
      "email": "contact@fast-delivery.com",
      "address": "456 Delivery St",
      "website": "https://fast-delivery.com",
      "state": "active"
    }
  ],
  "total": 1
}
```

## Error Handling

Tất cả các endpoint đều trả về response với format thống nhất:

**Success Response:**
```json
{
  "success": true,
  "data": [...],
  "total": 1
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created (for POST requests)
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Usage Examples

### JavaScript/Fetch
```javascript
// Get all brands
fetch('/api/physical-gift/brands')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Brands:', data.data);
    } else {
      console.error('Error:', data.error);
    }
  });

// Create new order
fetch('/api/physical-gift/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    program_id: 1,
    recipient_name: 'Nguyễn Văn A',
    recipient_phone: '0123456789',
    total_order_value: 1500000
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Order created:', data.data);
  } else {
    console.error('Error:', data.error);
  }
});
```

### cURL
```bash
# Get all brands
curl -X GET "http://your-odoo-domain.com/api/physical-gift/brands"

# Create new order
curl -X POST "http://your-odoo-domain.com/api/physical-gift/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "program_id": 1,
    "recipient_name": "Nguyễn Văn A",
    "recipient_phone": "0123456789",
    "total_order_value": 1500000
  }'
```

## Notes

1. Tất cả các endpoint đều sử dụng `sudo()` để bypass access rights
2. API hiện tại cho phép truy cập công khai, cần implement authentication cho production
3. Tất cả các response đều được format theo chuẩn JSON
4. Các trường ngày tháng được format theo định dạng ISO (YYYY-MM-DD)
5. Các trường datetime được format theo định dạng ISO (YYYY-MM-DD HH:MM:SS) 