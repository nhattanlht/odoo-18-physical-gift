# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftSupplier(models.Model):
    _name = 'physical.gift.supplier'
    _description = 'Physical Gift Supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Thông tin cơ bản
    name = fields.Char(
        string='Tên viết tắt',
        required=True,
        tracking=True,
        help='Tên viết tắt của nhà cung cấp'
    )
    
    full_name = fields.Char(
        string='Tên đầy đủ',
        required=True,
        tracking=True,
        help='Tên đầy đủ của nhà cung cấp'
    )
    
    representative_name = fields.Char(
        string='Tên người đại diện',
        tracking=True,
        help='Tên người đại diện của nhà cung cấp'
    )
    
    # Thông tin thuế và ngân hàng
    tax_code = fields.Char(
        string='MST',
        tracking=True,
        help='Mã số thuế của nhà cung cấp'
    )
    
    account_number = fields.Char(
        string='STK',
        tracking=True,
        help='Số tài khoản ngân hàng'
    )
    
    bank_name = fields.Char(
        string='Ngân hàng',
        tracking=True,
        help='Tên ngân hàng'
    )
    
    # Thông tin kho
    warehouse_code = fields.Char(
        string='Mã kho',
        tracking=True,
        help='Mã kho của nhà cung cấp'
    )
    
    # Trạng thái
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Trạng thái', default='active', tracking=True)
    
    active = fields.Boolean(
        default=True,
        help='Archived suppliers will not be displayed'
    )
    
    # Quan hệ với các model khác
    brand_ids = fields.Many2many(
        'physical.gift.brand',
        string='Thương hiệu cung cấp',
        help='Các thương hiệu mà nhà cung cấp này cung cấp'
    )
    
    item_ids = fields.One2many(
        'physical.gift.item',
        'supplier_id',
        string='Sản phẩm cung cấp'
    )
    
    # Thống kê
    brand_count = fields.Integer(
        'Số thương hiệu',
        compute='_compute_counts',
        store=True
    )
    
    item_count = fields.Integer(
        'Số sản phẩm',
        compute='_compute_counts',
        store=True
    )
    
    @api.depends('brand_ids', 'item_ids')
    def _compute_counts(self):
        for record in self:
            record.brand_count = len(record.brand_ids)
            record.item_count = len(record.item_ids)
    
    # Constraints
    _sql_constraints = [
        ('unique_supplier_name', 'unique(name)', 'Tên viết tắt nhà cung cấp phải là duy nhất!'),
        ('unique_supplier_tax_code', 'unique(tax_code)', 'Mã số thuế phải là duy nhất!')
    ]
    
    # Actions
    def action_activate(self):
        """Kích hoạt nhà cung cấp"""
        for record in self:
            record.state = 'active'
    
    def action_deactivate(self):
        """Tạm dừng nhà cung cấp"""
        for record in self:
            record.state = 'inactive'
    
    def action_view_brands(self):
        """Xem danh sách thương hiệu"""
        return {
            'name': _('Thương hiệu'),
            'type': 'ir.actions.act_window',
            'res_model': 'physical.gift.brand',
            'view_mode': 'list,form',
            'domain': [('supplier_ids', 'in', self.ids)],
            'context': {'default_supplier_ids': [(6, 0, self.ids)]}
        }
    
    def action_view_items(self):
        """Xem danh sách sản phẩm"""
        return {
            'name': _('Sản phẩm'),
            'type': 'ir.actions.act_window',
            'res_model': 'physical.gift.item',
            'view_mode': 'list,form',
            'domain': [('supplier_id', 'in', self.ids)],
            'context': {'default_supplier_id': self.id}
        }
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.name} - {record.full_name}"
            result.append((record.id, name))
        return result 