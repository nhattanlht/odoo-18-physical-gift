# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftShippingUnit(models.Model):
    _name = 'physical.gift.shipping.unit'
    _description = 'Physical Gift Shipping Unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Thông tin cơ bản
    name = fields.Char(
        string='Tên đơn vị vận chuyển',
        required=True,
        tracking=True,
        help='Tên đầy đủ của đơn vị vận chuyển'
    )
    
    code = fields.Char(
        string='Mã đơn vị vận chuyển',
        required=True,
        tracking=True,
        help='Mã định danh của đơn vị vận chuyển'
    )
    
    # Trạng thái
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Trạng thái', default='active', tracking=True)
    
    # Thông tin bổ sung
    description = fields.Text(
        string='Mô tả',
        tracking=True,
        help='Mô tả chi tiết về đơn vị vận chuyển'
    )
    
    contact_info = fields.Text(
        string='Thông tin liên hệ',
        tracking=True,
        help='Thông tin liên hệ của đơn vị vận chuyển'
    )
    
    website = fields.Char(
        string='Website',
        tracking=True,
        help='Website của đơn vị vận chuyển'
    )
    
    phone = fields.Char(
        string='Số điện thoại',
        tracking=True,
        help='Số điện thoại liên hệ'
    )
    
    email = fields.Char(
        string='Email',
        tracking=True,
        help='Email liên hệ'
    )
    
    address = fields.Text(
        string='Địa chỉ',
        tracking=True,
        help='Địa chỉ của đơn vị vận chuyển'
    )

    logo = fields.Binary(
        string='Logo',
        attachment=True,
        help='Logo thương hiệu'
    )
    
    # Quan hệ với các model khác
    program_ids = fields.Many2many(
        'physical.gift.program',
        string='Chương trình sử dụng',
        help='Các chương trình sử dụng đơn vị vận chuyển này'
    )
    
    # Thống kê
    program_count = fields.Integer(
        'Số chương trình',
        compute='_compute_counts',
        store=True
    )
    
    @api.depends('program_ids')
    def _compute_counts(self):
        for record in self:
            record.program_count = len(record.program_ids)
    
    # Constraints
    _sql_constraints = [
        ('unique_shipping_unit_code', 'unique(code)', 'Mã đơn vị vận chuyển phải là duy nhất!'),
        ('unique_shipping_unit_name', 'unique(name)', 'Tên đơn vị vận chuyển phải là duy nhất!')
    ]
    
    # Actions
    def action_activate(self):
        """Kích hoạt đơn vị vận chuyển"""
        for record in self:
            record.state = 'active'
    
    def action_deactivate(self):
        """Tạm dừng đơn vị vận chuyển"""
        for record in self:
            record.state = 'inactive'
    
    def action_view_programs(self):
        """Xem danh sách chương trình"""
        return {
            'name': _('Chương trình'),
            'type': 'ir.actions.act_window',
            'res_model': 'physical.gift.program',
            'view_mode': 'list,form',
            'domain': [('shipping_unit_ids', 'in', self.ids)],
            'context': {'default_shipping_unit_ids': [(6, 0, self.ids)]}
        }
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.code} - {record.name}"
            result.append((record.id, name))
        return result 