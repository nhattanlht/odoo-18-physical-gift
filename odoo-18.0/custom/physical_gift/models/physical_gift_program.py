# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftProgram(models.Model):
    _name = 'physical.gift.program'
    _description = 'Physical Gift Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Tên chương trình',
        required=True,
        tracking=True,
        help='Tên của chương trình quà tặng vật lý'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        required=True,
        default=lambda self: self.env.company,
        tracking=True
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
        help='Archived programs will not be displayed in the list'
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
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('closed', 'Đã đóng')
    ], string='Trạng thái', default='draft', tracking=True)
    
    gift_count = fields.Integer(
        string='Số lượng quà',
        compute='_compute_gift_count'
    )
    
    @api.depends('gift_ids')
    def _compute_gift_count(self):
        for record in self:
            record.gift_count = len(record.gift_ids)
    
    gift_ids = fields.One2many(
        'physical.gift.item',
        'program_id',
        string='Danh sách quà'
    )
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise UserError(_('Ngày bắt đầu không thể sau ngày kết thúc.'))
    
    def action_activate(self):
        """Kích hoạt chương trình"""
        for record in self:
            record.state = 'active'
    
    def action_deactivate(self):
        """Tạm dừng chương trình"""
        for record in self:
            record.state = 'inactive'
    
    def action_close(self):
        """Đóng chương trình"""
        for record in self:
            record.state = 'closed'
    
    def action_reset_to_draft(self):
        """Đặt lại về nháp"""
        for record in self:
            record.state = 'draft'
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"{record.name} ({record.company_id.name})"
            result.append((record.id, name))
        return result


class PhysicalGiftItem(models.Model):
    _name = 'physical.gift.item'
    _description = 'Physical Gift Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(
        string='Tên quà',
        required=True,
        tracking=True
    )
    
    program_id = fields.Many2one(
        'physical.gift.program',
        string='Chương trình',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Sản phẩm',
        tracking=True
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
    
    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price 