# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftOrder(models.Model):
    _name = 'physical.gift.order'
    _description = 'Physical Gift Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Thông tin cơ bản
    name = fields.Char(
        string='Mã đơn hàng',
        required=True,
        tracking=True,
        help='Mã đơn hàng'
    )
    
    program_id = fields.Many2one(
        'physical.gift.program',
        string='Chương trình',
        required=True,
        tracking=True,
        help='Chương trình liên quan'
    )
    
    product_name = fields.Char(
        string='Tên sản phẩm',
        required=True,
        tracking=True,
        help='Tên sản phẩm trong đơn hàng'
    )
    
    sku = fields.Char(
        string='SKU',
        tracking=True,
        help='Mã SKU sản phẩm'
    )
    
    original_sku = fields.Char(
        string='SKU gốc',
        tracking=True,
        help='Mã SKU gốc'
    )
    
    # Thông tin người nhận
    recipient_name = fields.Char(
        string='Tên người nhận',
        required=True,
        tracking=True,
        help='Tên người nhận hàng'
    )
    
    recipient_phone = fields.Char(
        string='Số điện thoại người nhận',
        required=True,
        tracking=True,
        help='Số điện thoại người nhận'
    )
    
    # Thông tin đơn hàng
    total_order_value = fields.Float(
        string='Tổng giá trị đơn hàng',
        required=True,
        tracking=True,
        help='Tổng giá trị đơn hàng'
    )
    
    voucher_code = fields.Char(
        string='Voucher code',
        tracking=True,
        help='Mã voucher'
    )
    
    # Thông tin vận chuyển
    shipping_unit_id = fields.Many2one(
        'physical.gift.shipping.unit',
        string='Đơn vị vận chuyển',
        tracking=True,
        help='Đơn vị vận chuyển'
    )
    
    waybill_code = fields.Char(
        string='Mã vận đơn',
        tracking=True,
        help='Mã vận đơn'
    )
    
    # Thông tin thanh toán
    payment_gateway = fields.Selection([
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('cash', 'Tiền mặt'),
        ('credit_card', 'Thẻ tín dụng'),
        ('e_wallet', 'Ví điện tử'),
        ('other', 'Khác')
    ], string='Cổng thanh toán', tracking=True)
    
    payment_status = fields.Selection([
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền')
    ], string='Trạng thái thanh toán', default='pending', tracking=True)
    
    transaction_code = fields.Char(
        string='Mã giao dịch',
        tracking=True,
        help='Mã giao dịch thanh toán'
    )
    
    # Thông tin sản phẩm
    product_type = fields.Selection([
        ('physical', 'Sản phẩm vật lý'),
        ('digital', 'Sản phẩm số'),
        ('service', 'Dịch vụ'),
        ('other', 'Khác')
    ], string='Loại sản phẩm', default='physical', tracking=True)
    
    # Thông tin thời gian
    order_time = fields.Datetime(
        string='Thời gian đặt hàng',
        required=True,
        default=fields.Datetime.now,
        tracking=True,
        help='Thời gian đặt hàng'
    )
    
    create_date = fields.Datetime(
        string='Thời gian tạo',
        default=fields.Datetime.now,
        tracking=True,
        help='Thời gian tạo đơn hàng'
    )
    
    # Trạng thái đơn hàng
    order_status = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('returned', 'Đã trả hàng')
    ], string='Trạng thái đơn hàng', default='draft', tracking=True)
    
    # Thông tin lỗi
    error_content = fields.Text(
        string='Nội dung lỗi',
        tracking=True,
        help='Nội dung lỗi nếu có'
    )
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động')
    ], string='Trạng thái', default='active', tracking=True)
    
    active = fields.Boolean(
        default=True,
        help='Archived orders will not be displayed'
    )
    
    # Thông tin bổ sung
    notes = fields.Text(
        string='Ghi chú',
        tracking=True,
        help='Ghi chú về đơn hàng'
    )
    
    # Quan hệ với các model khác
    import_id = fields.Many2one(
        'physical.gift.import',
        string='Nhập hàng liên quan',
        tracking=True,
        help='Nhập hàng liên quan'
    )
    
    # Actions
    def action_confirm(self):
        """Xác nhận đơn hàng"""
        for record in self:
            record.order_status = 'confirmed'
    
    def action_process(self):
        """Xử lý đơn hàng"""
        for record in self:
            record.order_status = 'processing'
    
    def action_ship(self):
        """Gửi hàng"""
        for record in self:
            record.order_status = 'shipped'
    
    def action_deliver(self):
        """Giao hàng"""
        for record in self:
            record.order_status = 'delivered'
    
    def action_cancel(self):
        """Hủy đơn hàng"""
        for record in self:
            record.order_status = 'cancelled'
    
    def action_return(self):
        """Trả hàng"""
        for record in self:
            record.order_status = 'returned'
    
    def action_reset_to_draft(self):
        """Đặt lại về nháp"""
        for record in self:
            record.order_status = 'draft'
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.name} - {record.recipient_name}"
            result.append((record.id, name))
        return result 