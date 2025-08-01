# Physical Gift Management Module

## Tổng quan

Module quản lý quà tặng vật lý (Physical Gift Management) là một ứng dụng Odoo toàn diện được thiết kế để quản lý các chương trình quà tặng vật lý, danh mục quà tặng, thương hiệu đối tác và cửa hàng.

## Tính năng chính

### 1. Quản lý chương trình quà tặng
- Tạo và quản lý các chương trình quà tặng vật lý
- Hỗ trợ đa ngôn ngữ (Tiếng Việt và Tiếng Anh)
- Theo dõi trạng thái chương trình (Nháp, Hoạt động, Không hoạt động, Đã đóng)
- Quản lý thông tin redeem (Brand và Store)
- Tính năng cập nhật chương trình với giao diện chuyên dụng

### 2. Quản lý thương hiệu đối tác
- **Thông tin cơ bản**: Tên thương hiệu, mã thương hiệu, website
- **Thông tin liên hệ**: Người liên hệ, số điện thoại, email, địa chỉ
- **Thông tin hợp tác**: Ngày bắt đầu hợp tác, số hợp đồng, tỷ lệ hoa hồng
- **Quản lý trạng thái**: Nháp, Hoạt động, Tạm ngưng, Không hoạt động
- **Thống kê**: Số lượng cửa hàng và chương trình liên quan
- **Hình ảnh**: Logo và hình ảnh đại diện thương hiệu

### 3. Quản lý danh mục quà tặng
- Hệ thống danh mục phân cấp (parent-child)
- Hỗ trợ đa ngôn ngữ
- Quản lý trạng thái và thứ tự hiển thị
- Hình ảnh và mô tả chi tiết

### 4. Quản lý cửa hàng
- Liên kết với thương hiệu
- Thông tin cơ bản và trạng thái hoạt động

### 5. Quản lý quà tặng vật lý
- Liên kết với chương trình và sản phẩm
- Tính toán giá trị và số lượng
- Theo dõi trạng thái

## Cấu trúc dữ liệu

### PhysicalGiftBrand (Thương hiệu)
```python
# Thông tin cơ bản
name = fields.Char('Tên thương hiệu', required=True)
name_en = fields.Char('Tên tiếng Anh')
code = fields.Char('Mã thương hiệu', required=True)

# Thông tin liên hệ
contact_person = fields.Char('Người liên hệ')
phone = fields.Char('Số điện thoại')
email = fields.Char('Email')
address = fields.Text('Địa chỉ')
website = fields.Char('Website')

# Thông tin hợp tác
partnership_date = fields.Date('Ngày bắt đầu hợp tác')
contract_number = fields.Char('Số hợp đồng')
commission_rate = fields.Float('Tỷ lệ hoa hồng (%)')

# Trạng thái và cấu hình
state = fields.Selection([
    ('draft', 'Nháp'),
    ('active', 'Hoạt động'),
    ('inactive', 'Không hoạt động'),
    ('suspended', 'Tạm ngưng')
], default='draft')

# Thống kê
store_count = fields.Integer('Số lượng cửa hàng', compute='_compute_store_count')
program_count = fields.Integer('Số lượng chương trình', compute='_compute_program_count')
```

### PhysicalGiftProgram (Chương trình)
```python
# Thông tin chương trình
name_vi = fields.Char('Tên Tiếng Việt', required=True)
name_en = fields.Char('Tên Tiếng Anh', required=True)
name = fields.Char('Tên chương trình', compute='_compute_name', store=True)

# Cấu hình redeem
brand_redeem_id = fields.Many2one('physical.gift.brand', 'Brand Redeem')
store_redeem_id = fields.Many2one('physical.gift.store', 'Store Redeem')
bill_number = fields.Char('Bill number')

# Trạng thái
state = fields.Selection([
    ('draft', 'Nháp'),
    ('active', 'Hoạt động'),
    ('inactive', 'Không hoạt động'),
    ('closed', 'Đã đóng')
], default='draft')
```

### PhysicalGiftCategory (Danh mục)
```python
# Thông tin cơ bản
name = fields.Char('Tên danh mục', required=True)
name_en = fields.Char('Tên tiếng Anh')
code = fields.Char('Mã danh mục')

# Phân cấp
parent_id = fields.Many2one('physical.gift.category', 'Danh mục cha')
child_ids = fields.One2many('physical.gift.category', 'parent_id', 'Danh mục con')
complete_name = fields.Char('Tên đầy đủ', compute='_compute_complete_name', store=True)

# Trạng thái
state = fields.Selection([
    ('active', 'Active'),
    ('inactive', 'Inactive')
], default='active')
```

## Giao diện

### 1. Quản lý thương hiệu
- **Tree View**: Hiển thị danh sách với thông tin cơ bản, trạng thái và thống kê
- **Form View**: Giao diện chi tiết với các tab thông tin
- **Kanban View**: Hiển thị dạng card với hình ảnh và thông tin tổng quan
- **Search View**: Tìm kiếm và lọc theo nhiều tiêu chí

### 2. Cập nhật chương trình
- Giao diện chuyên dụng cho việc cập nhật chương trình
- Phân chia rõ ràng: "Thông tin chương trình chung" và "Cấu hình thông tin redeem"
- Tích hợp với hệ thống thương hiệu và cửa hàng

### 3. Quản lý danh mục
- Tree view phân cấp
- Form view với thông tin chi tiết
- Hỗ trợ kéo thả để sắp xếp

## Bảo mật

Module sử dụng hệ thống phân quyền của Odoo:

### Nhóm người dùng
- `group_physical_gift_user`: Quyền đọc dữ liệu
- `group_physical_gift_manager`: Quyền đầy đủ (đọc, ghi, tạo, xóa)

### Quyền truy cập
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_physical_gift_brand_user,physical.gift.brand.user,model_physical_gift_brand,group_physical_gift_user,1,0,0,0
access_physical_gift_brand_manager,physical.gift.brand.manager,model_physical_gift_brand,group_physical_gift_manager,1,1,1,1
```

## Dữ liệu mẫu

### Thương hiệu mẫu
1. **Home Delivery** (HD001) - Dịch vụ giao hàng tận nhà
2. **Physical Gift** (PG002) - Quà tặng vật lý chất lượng cao
3. **E-commerce** (EC003) - Nền tảng thương mại điện tử
4. **Fashion Style** (FS004) - Thời trang cao cấp
5. **Tech Solutions** (TS005) - Sản phẩm công nghệ
6. **Food & Beverage** (FB006) - Thực phẩm và đồ uống
7. **Beauty & Cosmetics** (BC007) - Mỹ phẩm và làm đẹp
8. **Sports & Fitness** (SF008) - Thể thao và fitness
9. **Home & Living** (HL009) - Trang trí nhà cửa
10. **Books & Education** (BE010) - Sách và giáo dục

### Danh mục mẫu
- Danh mục phân cấp với 14 danh mục con
- Hỗ trợ đa ngôn ngữ
- Các trạng thái khác nhau

## Cài đặt và sử dụng

### 1. Cài đặt module
```bash
# Cập nhật module
python odoo-bin -d your_database -u physical_gift
```

### 2. Truy cập tính năng
- **Physical Gift** → **Cấu hình** → **Thương hiệu**: Quản lý thương hiệu
- **Physical Gift** → **Chương trình** → **Danh sách chương trình**: Quản lý chương trình
- **Physical Gift** → **Chương trình** → **Cập nhật chương trình**: Cập nhật chương trình
- **Physical Gift** → **Danh mục** → **Danh sách danh mục**: Quản lý danh mục

### 3. Tạo thương hiệu mới
1. Vào **Physical Gift** → **Cấu hình** → **Thương hiệu**
2. Click **Tạo**
3. Điền thông tin cơ bản:
   - Tên thương hiệu
   - Mã thương hiệu (duy nhất)
   - Thông tin liên hệ
4. Cấu hình thông tin hợp tác
5. Upload logo và hình ảnh
6. Lưu và kích hoạt

### 4. Quản lý trạng thái
- **Nháp**: Thương hiệu mới tạo
- **Hoạt động**: Thương hiệu đang hợp tác
- **Tạm ngưng**: Tạm thời ngưng hợp tác
- **Không hoạt động**: Đã chấm dứt hợp tác

## Tính năng nâng cao

### 1. Tìm kiếm thông minh
- Tìm kiếm theo tên, mã, người liên hệ
- Lọc theo trạng thái, ngày hợp tác, tỷ lệ hoa hồng
- Nhóm theo nhiều tiêu chí

### 2. Thống kê và báo cáo
- Số lượng cửa hàng và chương trình liên quan
- Tỷ lệ hoa hồng và thông tin hợp tác
- Theo dõi hiệu suất thương hiệu

### 3. Tích hợp hệ thống
- Liên kết với chương trình quà tặng
- Quản lý cửa hàng theo thương hiệu
- Tích hợp với hệ thống sản phẩm Odoo

## Tùy chỉnh và mở rộng

### 1. Thêm trường mới
```python
# Trong model PhysicalGiftBrand
new_field = fields.Char('Trường mới', tracking=True)
```

### 2. Tùy chỉnh giao diện
- Chỉnh sửa file XML view
- Thêm CSS tùy chỉnh
- Tạo action mới

### 3. Thêm tính năng mới
- Tạo method mới trong model
- Thêm button action
- Tạo wizard hoặc report

## Hỗ trợ và liên hệ

- **Tác giả**: Your Company
- **Website**: https://www.yourcompany.com
- **Email**: support@yourcompany.com
- **License**: LGPL-3

## Changelog

### Version 1.0
- ✅ Quản lý thương hiệu đối tác hoàn chỉnh
- ✅ Giao diện Tree, Form, Kanban cho thương hiệu
- ✅ Hệ thống tìm kiếm và lọc nâng cao
- ✅ Dữ liệu mẫu đầy đủ
- ✅ CSS tùy chỉnh cho giao diện đẹp
- ✅ Tích hợp với hệ thống chương trình và cửa hàng
- ✅ Quản lý trạng thái và thống kê
- ✅ Hỗ trợ đa ngôn ngữ
- ✅ Bảo mật và phân quyền 