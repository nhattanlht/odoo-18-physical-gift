# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PhysicalGiftItem(models.Model):
    _name = 'physical.gift.item'
    _description = 'Physical Gift Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(
        string='Tên quà',
        required=True,
        tracking=True
    )
    
    brand_id = fields.Many2one(
        'physical.gift.brand',
        string='Thương hiệu',
        tracking=True
    )
    
    category_id = fields.Many2one(
        'physical.gift.category',
        string='Danh mục',
        tracking=True
    )
    
    supplier_id = fields.Many2one(
        'physical.gift.supplier',
        string='Nhà cung cấp',
        tracking=True
    )

    image = fields.Image(
        string="Hình ảnh",
    )
    
    quantity = fields.Integer(
        string='Số lượng',
        default=1,
        tracking=True
    )
    
    unit_price = fields.Float(
        string='Đơn giá',
        tracking=True
    )
    
    total_price = fields.Float(
        string='Tổng giá',
        compute='_compute_total_price',
        store=True
    )
    
    active = fields.Boolean(
        default=True,
        help='Archived items will not be displayed'
    )
    
    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price 