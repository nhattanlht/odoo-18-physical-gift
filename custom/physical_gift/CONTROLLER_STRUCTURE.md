# Cấu Trúc Chia File Controllers

## Tổng Quan
Khi có nhiều API cho các model khác nhau, chúng ta chia file trong thư mục `controllers` để dễ quản lý và bảo trì.

## Cấu Trúc Thư Mục
```
custom/physical_gift/controllers/
├── __init__.py              # Import tất cả controllers
├── main.py                  # File chính (có thể để trống hoặc chứa logic chung)
├── brand_controller.py      # API cho Physical Gift Brand
├── category_controller.py   # API cho Physical Gift Category
├── item_controller.py       # API cho Physical Gift Item
├── order_controller.py      # API cho Physical Gift Order
├── program_controller.py    # API cho Physical Gift Program
├── supplier_controller.py   # API cho Physical Gift Supplier
└── shipping_controller.py   # API cho Physical Gift Shipping Unit
```

## Quy Tắc Đặt Tên
- **File controller**: `{model_name}_controller.py`
- **Class controller**: `{ModelName}Controller`
- **Route pattern**: `/api/physical-gift/{model-name}`

## Ví Dụ Thêm Controller Mới

### 1. Tạo file controller mới
```python
# custom/physical_gift/controllers/store_controller.py
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class StoreController(http.Controller):
    """API Controller cho Physical Gift Store"""
    
    @http.route('/api/physical-gift/stores', type='http', auth='public', methods=['GET'], csrf=False)
    def get_stores(self, **kwargs):
        """Lấy danh sách cửa hàng"""
        try:
            # Logic xử lý
            pass
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
```

### 2. Cập nhật __init__.py
```python
# custom/physical_gift/controllers/__init__.py
from . import main
from . import brand_controller
from . import category_controller
from . import item_controller
from . import order_controller
from . import program_controller
from . import supplier_controller
from . import shipping_controller
from . import store_controller  # Thêm dòng này
```

## Lợi Ích Của Việc Chia File

### 1. Dễ Quản Lý
- Mỗi model có file controller riêng
- Dễ tìm và sửa code
- Tránh file quá lớn

### 2. Dễ Bảo Trì
- Sửa lỗi chỉ ảnh hưởng đến model cụ thể
- Dễ thêm tính năng mới
- Code rõ ràng, có cấu trúc

### 3. Dễ Mở Rộng
- Thêm model mới chỉ cần tạo file mới
- Không ảnh hưởng đến code cũ
- Dễ test từng phần

### 4. Team Development
- Nhiều người có thể làm việc song song
- Giảm conflict khi merge code
- Dễ phân chia công việc

## Quy Tắc Code

### 1. Import
```python
from odoo import http
from odoo.http import request
import json
```

### 2. Class Structure
```python
class ModelNameController(http.Controller):
    """API Controller cho Physical Gift ModelName"""
    
    @http.route('/api/physical-gift/model-name', type='http', auth='public', methods=['GET'], csrf=False)
    def get_models(self, **kwargs):
        """Lấy danh sách model"""
        try:
            # Logic xử lý
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(data)
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
```

### 3. Error Handling
- Luôn sử dụng try-catch
- Trả về JSON format nhất quán
- Log lỗi để debug

### 4. Response Format
```python
# Success response
{
    'success': True,
    'data': [...],
    'total': 10
}

# Error response
{
    'success': False,
    'error': 'Error message'
}
```

## Tips

### 1. Khi Thêm Model Mới
1. Tạo file `{model_name}_controller.py`
2. Thêm import vào `__init__.py`
3. Test API endpoint
4. Cập nhật documentation

### 2. Khi Sửa API
1. Chỉ sửa file controller tương ứng
2. Test kỹ trước khi deploy
3. Cập nhật documentation nếu cần

### 3. Khi Debug
1. Kiểm tra log Odoo
2. Test từng endpoint riêng biệt
3. Sử dụng Postman hoặc curl để test

## Ví Dụ Thực Tế

### Thêm API cho Store Model
```python
# custom/physical_gift/controllers/store_controller.py
@http.route('/api/physical-gift/stores', type='http', auth='public', methods=['GET'], csrf=False)
def get_stores(self, **kwargs):
    """Lấy danh sách cửa hàng"""
    try:
        limit = int(kwargs.get('limit', 100))
        offset = int(kwargs.get('offset', 0))
        
        domain = [('active', '=', True)]
        
        if kwargs.get('brand_id'):
            domain.append(('brand_id', '=', int(kwargs.get('brand_id'))))
        
        stores = request.env['physical.gift.store'].sudo().search(
            domain, 
            limit=limit, 
            offset=offset,
            order='name'
        )
        
        data = []
        for store in stores:
            data.append({
                'id': store.id,
                'name': store.name,
                'brand_id': store.brand_id.id if store.brand_id else None,
                'brand_name': store.brand_id.name if store.brand_id else None,
                'active': store.active,
            })
        
        return json.dumps({
            'success': True,
            'data': data,
            'total': len(stores)
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=False)
```

Cấu trúc này giúp code dễ quản lý, bảo trì và mở rộng trong tương lai. 