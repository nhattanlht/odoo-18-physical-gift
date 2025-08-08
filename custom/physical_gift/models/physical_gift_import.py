# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftImport(models.Model):
    _name = 'physical.gift.import'
    _description = 'Physical Gift Import'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'import_date desc'

    # Thông tin cơ bản
    name = fields.Char(
        string='Tên sản phẩm',
        required=True,
        tracking=True,
        help='Tên sản phẩm nhập hàng'
    )
    
    sku = fields.Char(
        string='SKU',
        required=True,
        tracking=True,
        help='Mã SKU sản phẩm'
    )
    
    points = fields.Integer(
        string='Điểm',
        default=0,
        tracking=True,
        help='Điểm của sản phẩm'
    )
    
    import_date = fields.Date(
        string='Thời gian nhập',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help='Ngày nhập hàng'
    )
    
    # Thông tin giá
    import_price_excl_vat = fields.Float(
        string='Giá nhập (chưa VAT)',
        required=True,
        tracking=True,
        help='Giá nhập hàng chưa bao gồm VAT'
    )
    
    sale_price_incl_vat = fields.Float(
        string='Giá bán (VAT)',
        required=True,
        tracking=True,
        help='Giá bán bao gồm VAT'
    )
    
    vat_percentage = fields.Float(
        string='VAT (%)',
        default=0.0,
        tracking=True,
        help='Phần trăm VAT'
    )
    
    # Quan hệ với các model khác
    supplier_id = fields.Many2one(
        'physical.gift.supplier',
        string='Nhà cung cấp',
        required=True,
        tracking=True,
        help='Nhà cung cấp sản phẩm'
    )
    
    program_id = fields.Many2one(
        'physical.gift.program',
        string='Chương trình',
        required=True,
        tracking=True,
        help='Chương trình liên quan'
    )
    
    item_id = fields.Many2one(
        'physical.gift.item',
        string='Sản phẩm',
        tracking=True,
        help='Sản phẩm liên quan'
    )
    
    # Thông tin số lượng
    import_quantity = fields.Integer(
        string='Số lượng nhập',
        required=True,
        default=1,
        tracking=True,
        help='Số lượng nhập hàng'
    )
    
    export_return_quantity = fields.Integer(
        string='Số lượng xuất trả',
        default=0,
        tracking=True,
        help='Số lượng xuất trả'
    )
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft', tracking=True)
    
    # Thông tin bổ sung
    notes = fields.Text(
        string='Ghi chú',
        tracking=True,
        help='Ghi chú về việc nhập hàng'
    )
    
    # Constraints
    _sql_constraints = [
        ('unique_import_sku', 'unique(sku)', 'Mã SKU phải là duy nhất!')
    ]
    
    # Actions
    def action_confirm(self):
        """Xác nhận nhập hàng"""
        for record in self:
            record.state = 'confirmed'

    def action_done(self):
        """Hoàn thành nhập hàng và cộng tồn kho"""
        for record in self:
            if not record.item_id:
                raise UserError(_("Vui lòng chọn sản phẩm liên quan trước khi hoàn thành."))

            # Cộng thêm số lượng nhập vào số lượng sản phẩm
            record.item_id.quantity += record.import_quantity - record.export_return_quantity

            record.state = 'done'
    
    def action_cancel(self):
        """Hủy nhập hàng"""
        for record in self:
            record.state = 'cancelled'
    
    def action_reset_to_draft(self):
        """Đặt lại về nháp"""
        for record in self:
            record.state = 'draft'
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.sku} - {record.name}"
            result.append((record.id, name))
        return result 