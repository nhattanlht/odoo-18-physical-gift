# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PhysicalGiftProgram(models.Model):
    _name = 'physical.gift.program'
    _description = 'Physical Gift Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    # Thông tin chương trình chung
    name_vi = fields.Char(
        string='Tên Tiếng Việt',
        required=True,
        tracking=True,
        help='Tên chương trình bằng tiếng Việt'
    )
    
    name_en = fields.Char(
        string='Tên Tiếng Anh',
        required=True,
        tracking=True,
        help='Tên chương trình bằng tiếng Anh'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        required=True,
        default=lambda self: self.env.company,
        tracking=True
    )
    
    order_creator_id = fields.Many2one(
        'res.users',
        string='Người tạo đơn hàng',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )
    
    # Cấu hình thông tin redeem
    brand_redeem_id = fields.Many2one(
        'physical.gift.brand',
        string='Brand Redeem',
        required=True,
        tracking=True,
        help='Brand redeem cho chương trình'
    )
    
    store_redeem_id = fields.Many2one(
        'physical.gift.store',
        string='Store Redeem',
        required=True,
        tracking=True,
        help='Store redeem cho chương trình'
    )
    
    bill_number = fields.Char(
        string='Bill number',
        tracking=True,
        help='Số bill của chương trình'
    )
    
    creator_id = fields.Many2one(
        'res.users',
        string='Người tạo',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )

    active = fields.Boolean(
        default=True,
        help='Thương hiệu không hoạt động sẽ không hiển thị'
    )
    
    description = fields.Text(
        string='Mô tả',
        tracking=True
    )
    
    start_date = fields.Date(
        string='Ngày bắt đầu',
        tracking=True
    )
    
    end_date = fields.Date(
        string='Ngày kết thúc',
        tracking=True
    )
    
    # Danh mục trong chương trình
    category_ids = fields.Many2many('physical.gift.category', string='Danh mục')
    
    # Đơn vị vận chuyển
    shipping_unit_ids = fields.Many2many('physical.gift.shipping.unit', string='Đơn vị vận chuyển')
    
    # Thống kê
    category_count = fields.Integer('Số danh mục', compute='_compute_counts', store=True)
    shipping_unit_count = fields.Integer('Số đơn vị vận chuyển', compute='_compute_counts', store=True)
    
    @api.depends('category_ids', 'shipping_unit_ids')
    def _compute_counts(self):
        for record in self:
            record.category_count = len(record.category_ids)
            record.shipping_unit_count = len(record.shipping_unit_ids)

    
    @api.depends('name_vi', 'name_en')
    def _compute_name(self):
        for record in self:
            if record.name_vi and record.name_en:
                record.name = f"{record.name_vi} / {record.name_en}"
            elif record.name_vi:
                record.name = record.name_vi
            elif record.name_en:
                record.name = record.name_en
            else:
                record.name = ''

    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise UserError(_('Ngày bắt đầu không thể sau ngày kết thúc.'))
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.name_vi or record.name_en} ({record.company_id.name})"
            result.append((record.id, name))
        return result

class PhysicalGiftStore(models.Model):
    _name = 'physical.gift.store'
    _description = 'Physical Gift Store'
    _order = 'name'

    name = fields.Char(
        string='Tên Store',
        required=True
    )

    code = fields.Char(
        string='Mã Store',
        required=True
    )

    brand_id = fields.Many2one(
        'physical.gift.brand',
        string='Brand',
        required=True
    )

    active = fields.Boolean(
        default=True
    )

    _sql_constraints = [
        ('unique_store_code', 'unique(code)', 'Mã store phải là duy nhất!')
    ]


