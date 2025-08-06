# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftBrand(models.Model):
    _name = 'physical.gift.brand'
    _description = 'Physical Gift Brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    
    # Thông tin cơ bản
    name = fields.Char(
        string='Tên thương hiệu',
        required=True,
        tracking=True,
        help='Tên thương hiệu quà tặng vật lý'
    )
    
    name_en = fields.Char(
        string='Tên tiếng Anh',
        tracking=True,
        help='Tên thương hiệu bằng tiếng Anh'
    )
    
    code = fields.Char(
        string='Mã thương hiệu',
        required=True,
        tracking=True,
        help='Mã định danh thương hiệu'
    )
    
    # Thông tin liên hệ
    contact_person = fields.Char(
        string='Người liên hệ',
        tracking=True,
        help='Tên người đại diện thương hiệu'
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
        help='Địa chỉ trụ sở chính'
    )
    
    # Thông tin kinh doanh
    website = fields.Char(
        string='Website',
        tracking=True,
        help='Website chính thức của thương hiệu'
    )
    
    description = fields.Text(
        string='Mô tả',
        tracking=True,
        help='Mô tả chi tiết về thương hiệu'
    )
    
    # Hình ảnh và logo
    logo = fields.Binary(
        string='Logo',
        attachment=True,
        help='Logo thương hiệu'
    )
    
    # Trạng thái và cấu hình
    sequence = fields.Integer(
        default=10,
        help='Thứ tự hiển thị'
    )
    
    # Thông tin hợp tác
    partnership_date = fields.Date(
        string='Ngày bắt đầu hợp tác',
        tracking=True,
        help='Ngày bắt đầu hợp tác với thương hiệu'
    )
    
    contract_number = fields.Char(
        string='Số hợp đồng',
        tracking=True,
        help='Số hợp đồng hợp tác'
    )
    
    commission_rate = fields.Float(
        string='Tỷ lệ hoa hồng (%)',
        tracking=True,
        help='Tỷ lệ hoa hồng cho thương hiệu'
    )
    
    # Thống kê
    store_count = fields.Integer(
        string='Số lượng cửa hàng',
        compute='_compute_store_count',
        store=True
    )
    
    program_count = fields.Integer(
        string='Số lượng chương trình',
        compute='_compute_program_count',
        store=True
    )
    
    # Quan hệ
    store_ids = fields.One2many(
        'physical.gift.store',
        'brand_id',
        string='Cửa hàng'
    )
    
    program_ids = fields.One2many(
        'physical.gift.program',
        'brand_redeem_id',
        string='Chương trình'
    )
    
    supplier_ids = fields.Many2many(
        'physical.gift.supplier',
        string='Nhà cung cấp',
        help='Các nhà cung cấp cho thương hiệu này'
    )
    
    # Constraints
    _sql_constraints = [
        ('unique_brand_code', 'unique(code)', 'Mã thương hiệu phải là duy nhất!'),
        ('unique_brand_name', 'unique(name)', 'Tên thương hiệu phải là duy nhất!')
    ]

    active = fields.Boolean(
        default=True,
        help='Thương hiệu không hoạt động sẽ không hiển thị'
    )

    status_display = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        string="Status Display",
        compute="_compute_status_display",
        store=False,
    )

    @api.depends('active')
    def _compute_status_display(self):
        for rec in self:
            rec.status_display = 'active' if rec.active else 'inactive'

    @api.depends('store_ids')
    def _compute_store_count(self):
        for record in self:
            record.store_count = len(record.store_ids)
    
    @api.depends('program_ids')
    def _compute_program_count(self):
        for record in self:
            record.program_count = len(record.program_ids)
    
    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        for record in self:
            if record.commission_rate and (record.commission_rate < 0 or record.commission_rate > 100):
                raise UserError(_('Tỷ lệ hoa hồng phải từ 0% đến 100%'))
    
    # Actions
    def action_view_programs(self):
        """Xem danh sách chương trình"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chương trình của %s' % self.name,
            'res_model': 'physical.gift.program',
            'view_mode': 'list,form',
            'domain': [('brand_redeem_id', '=', self.id)],
            'context': {'default_brand_redeem_id': self.id}
        }
    
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            if record.name_en:
                name += f" | {record.name_en}"
            result.append((record.id, name))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|',
                     ('name', operator, name),
                     ('name_en', operator, name),
                     ('code', operator, name),
                     ('contact_person', operator, name)]
        return self.search(domain + args, limit=limit).name_get() 