# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftCategory(models.Model):
    _name = 'physical.gift.category'
    _description = 'Physical Gift Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Tên danh mục',
        required=True,
        tracking=True,
        help='Tên danh mục quà vật lý'
    )
    
    name_en = fields.Char(
        string='Tên tiếng Anh',
        tracking=True,
        help='Tên danh mục bằng tiếng Anh'
    )
    
    code = fields.Char(
        string='Mã danh mục',
        tracking=True,
        help='Mã định danh danh mục'
    )
    
    complete_name = fields.Char(
        string='Tên đầy đủ',
        compute='_compute_complete_name',
        store=True,
        recursive=True
    )
    
    parent_id = fields.Many2one(
        'physical.gift.category',
        string='Danh mục cha',
        index=True,
        ondelete='cascade',
        tracking=True
    )
    
    child_ids = fields.One2many(
        'physical.gift.category',
        'parent_id',
        string='Danh mục con'
    )
    
    parent_path = fields.Char(
        index=True
    )
    
    sequence = fields.Integer(
        default=10,
        help='Thứ tự hiển thị'
    )
    
    active = fields.Boolean(
        default=True,
        help='Archived categories will not be displayed'
    )
    
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Trạng thái', default='active', tracking=True)
    
    description = fields.Text(
        string='Mô tả',
        tracking=True
    )
    
    image = fields.Binary(
        string='Hình ảnh',
        attachment=True
    )
    
    @api.depends('name', 'name_en', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
    
    @api.constrains('parent_id')
    def _check_parent_id(self):
        if self._has_cycle():
            raise UserError(_('Bạn không thể tạo danh mục con cho chính nó.'))
    
    def action_activate(self):
        """Kích hoạt danh mục"""
        for record in self:
            record.state = 'active'
    
    def action_deactivate(self):
        """Tạm dừng danh mục"""
        for record in self:
            record.state = 'inactive'
    
    def action_update(self):
        """Cập nhật danh mục"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật danh mục',
            'res_model': 'physical.gift.category',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f"[{record.id}] {record.name}"
            if record.name_en:
                name += f" | {record.name_en}"
            result.append((record.id, name))
        return result


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
    
    # Các trường cũ giữ lại
    name = fields.Char(
        string='Tên chương trình',
        compute='_compute_name',
        store=True,
        help='Tên của chương trình quà tặng vật lý'
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
            name = f"{record.name_vi or record.name_en} ({record.company_id.name})"
            result.append((record.id, name))
        return result


class PhysicalGiftBrand(models.Model):
    _name = 'physical.gift.brand'
    _description = 'Physical Gift Brand'
    _order = 'name'
    
    name = fields.Char(
        string='Tên Brand',
        required=True
    )
    
    code = fields.Char(
        string='Mã Brand',
        required=True
    )
    
    active = fields.Boolean(
        default=True
    )
    
    _sql_constraints = [
        ('unique_brand_code', 'unique(code)', 'Mã brand phải là duy nhất!')
    ]


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


 