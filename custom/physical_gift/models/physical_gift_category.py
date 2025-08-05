# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PhysicalGiftCategory(models.Model):
    _name = 'physical.gift.category'
    _description = 'Physical Gift Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char('Tên danh mục', required=True, tracking=True)
    name_en = fields.Char('Tên tiếng Anh', tracking=True)
    code = fields.Char('Mã danh mục', required=True, tracking=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã danh mục phải là duy nhất!')
    ]
    

    
    # Thông tin cơ bản
    description = fields.Text('Mô tả')
    description_en = fields.Text('Mô tả tiếng Anh')
    
    # Cấu trúc phân cấp
    parent_id = fields.Many2one('physical.gift.category', string='Danh mục cha')
    child_ids = fields.One2many('physical.gift.category', 'parent_id', string='Danh mục con')
    

    
    # Sản phẩm trong danh mục
    item_ids = fields.One2many('physical.gift.item', 'category_id', string='Danh sách sản phẩm')
    
    # Chương trình liên quan
    program_ids = fields.Many2many('physical.gift.program', string='Chương trình')
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động')
    ], string='Trạng thái', default='draft', tracking=True)
    
    # Thống kê
    sequence = fields.Integer('Thứ tự', default=10)
    active = fields.Boolean('Hoạt động', default=True)
    
    # Liên kết
    item_count = fields.Integer('Số sản phẩm', compute='_compute_counts', store=True)
    program_count = fields.Integer('Số chương trình', compute='_compute_counts', store=True)
    
    @api.depends('item_ids', 'program_ids')
    def _compute_counts(self):
        for record in self:
            record.item_count = len(record.item_ids)
            record.program_count = len(record.program_ids)
    

    

    
    def action_activate(self):
        self.write({'state': 'active'})
    
    def action_deactivate(self):
        self.write({'state': 'inactive'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_close(self):
        self.write({'state': 'inactive'})
    

    
 