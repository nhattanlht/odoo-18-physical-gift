# Hướng Dẫn Debug API Physical Gift

## Lỗi 404 - URL Not Found

### Nguyên nhân có thể:
1. **Module chưa được cài đặt**
2. **Controllers chưa được import**
3. **URL sai**
4. **Port sai**
5. **Server chưa restart**

### Các bước khắc phục:

#### 1. Kiểm tra URL đúng
```
✅ ĐÚNG: http://localhost:8069/api/physical-gift/brands
❌ SAI:  http://localhost:8080/api/physical-gift/brands
❌ SAI:  http://localhost:3000/api/physical-gift/brands
```

#### 2. Restart Odoo Server
```bash
# Dừng server (Ctrl+C)
# Chạy lại với update module
python odoo-bin -d your_database_name -u physical_gift
```

#### 3. Test từng endpoint

**Test 1 - API cơ bản:**
```
GET http://localhost:8069/api/test
```

**Test 2 - Physical Gift API:**
```
GET http://localhost:8069/api/physical-gift/test
```

**Test 3 - Brand API:**
```
GET http://localhost:8069/api/physical-gift/brands
```

#### 4. Kiểm tra module trong Odoo
1. Vào **Apps**
2. Tìm "Physical Gift Management"
3. Đảm bảo status là **Installed**

#### 5. Kiểm tra log
```bash
python odoo-bin -d your_database_name -u physical_gift --log-level=debug
```

### Cấu trúc file đã được tạo:

```
custom/physical_gift/
├── __init__.py                    # Import models và controllers
├── models/
│   └── __init__.py               # Import tất cả models + controllers
├── controllers/
│   ├── __init__.py               # Import tất cả controllers
│   ├── test_controller.py        # Test API
│   ├── brand_controller.py       # Brand API
│   ├── category_controller.py    # Category API
│   ├── item_controller.py        # Item API
│   ├── order_controller.py       # Order API
│   ├── program_controller.py     # Program API
│   ├── supplier_controller.py    # Supplier API
│   └── shipping_controller.py    # Shipping API
```

### Test trong Postman:

#### Headers:
```
Content-Type: application/json
Accept: application/json
```

#### Endpoints:
```
GET  http://localhost:8069/api/test
GET  http://localhost:8069/api/physical-gift/test
GET  http://localhost:8069/api/physical-gift/brands
GET  http://localhost:8069/api/physical-gift/categories
GET  http://localhost:8069/api/physical-gift/items
GET  http://localhost:8069/api/physical-gift/programs
GET  http://localhost:8069/api/physical-gift/orders
GET  http://localhost:8069/api/physical-gift/suppliers
GET  http://localhost:8069/api/physical-gift/shipping-units
```

### Nếu vẫn lỗi:

1. **Kiểm tra database name** - Đảm bảo database tồn tại
2. **Kiểm tra port** - Mặc định là 8069
3. **Kiểm tra firewall** - Đảm bảo port không bị chặn
4. **Kiểm tra Odoo version** - Đảm bảo tương thích với Odoo 18.0 