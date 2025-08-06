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
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã danh mục phải là duy nhất!')
    ]

    # Thông tin cơ bản
    description = fields.Text('Mô tả')
    description_en = fields.Text('Mô tả tiếng Anh')
    image = fields.Image('Ảnh đại diện', max_width=512, max_height=512)

    # Sản phẩm trong danh mục
    item_ids = fields.One2many('physical.gift.item', 'category_id', string='Danh sách sản phẩm')

    # Chương trình liên quan
    program_ids = fields.Many2many('physical.gift.program', string='Chương trình')

    # Thống kê
    sequence = fields.Integer('Thứ tự', default=10)

    # Liên kết
    item_count = fields.Integer('Số sản phẩm', compute='_compute_counts', store=True)
    program_count = fields.Integer('Số chương trình', compute='_compute_counts', store=True)

    @api.depends('item_ids', 'program_ids')
    def _compute_counts(self):
        for record in self:
            record.item_count = len(record.item_ids)
            record.program_count = len(record.program_ids)

    def toggle_active(self):
        """
        Lưu trữ hoặc bỏ lưu trữ các bản ghi bằng cách đảo ngược trường 'active'.
        """
        for record in self:
            record.active = not record.active

    def action_open_items(self):
        """
        Trả về một action để mở cửa sổ hiển thị các sản phẩm
        thuộc danh mục này.
        """
        self.ensure_one()
        return {
            'name': _('Sản phẩm'),
            'type': 'ir.actions.act_window',
            'res_model': 'physical.gift.item',
            'view_mode': 'tree,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id}
        }