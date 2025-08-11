# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PhysicalGiftImport(models.Model):
    _name = 'physical.gift.import'
    _description = 'Phiếu nhập hàng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'import_date desc'

    name = fields.Char(
        string='Số phiếu',
        required=True,
        default='New',
        tracking=True
    )

    import_date = fields.Date(
        string='Ngày nhập',
        default=fields.Date.today,
        required=True,
        tracking=True
    )

    supplier_id = fields.Many2one(
        'physical.gift.supplier',
        string='Nhà cung cấp',
        required=True,
        tracking=True,
        domain=[('state', '=', 'active')]
    )

    program_id = fields.Many2one(
        'physical.gift.program',
        string='Chương trình',
        required=True,
        tracking=True,
        domain=[('active', '=', True)]
    )

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], default='draft', tracking=True)

    notes = fields.Text(string='Ghi chú', tracking=True)

    # Liên kết tới chi tiết nhập hàng
    line_ids = fields.One2many(
        'physical.gift.import.line',
        'import_id',
        string='Chi tiết nhập hàng'
    )

    # Số dòng hàng (tính toán)
    line_count = fields.Integer(
        string='Số dòng hàng',
        compute='_compute_line_count',
        store=False
    )

    @api.depends('line_ids')
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)

    # ================= Actions ================= #
    def action_confirm(self):
        """Xác nhận phiếu nhập"""
        for record in self:
            if not record.line_ids:
                raise UserError(_("Phiếu nhập phải có ít nhất 1 dòng hàng."))
            record.state = 'confirmed'

    def action_done(self):
        """Hoàn thành phiếu nhập và cộng tồn kho"""
        for record in self:
            if record.state != 'confirmed':
                raise UserError(_("Chỉ có thể hoàn thành khi phiếu đang ở trạng thái Đã xác nhận."))

            for line in record.line_ids:
                if not line.item_id:
                    raise UserError(_("Vui lòng chọn sản phẩm cho tất cả dòng hàng."))
                delta_qty = line.import_quantity - line.export_return_quantity
                line.item_id.sudo().write({'quantity': line.item_id.quantity + delta_qty})

            record.state = 'done'

    def action_cancel(self):
        """Hủy phiếu nhập"""
        for record in self:
            record.state = 'cancelled'

    def action_reset_to_draft(self):
        """Đặt lại về Nháp"""
        for record in self:
            record.state = 'draft'


class PhysicalGiftImportLine(models.Model):
    _name = 'physical.gift.import.line'
    _description = 'Dòng hàng nhập'

    import_id = fields.Many2one(
        'physical.gift.import',
        string='Phiếu nhập',
        required=True,
        ondelete='cascade'
    )

    item_id = fields.Many2one(
        'physical.gift.item',
        string='Sản phẩm',
        required=True,
        domain=[('active', '=', True)]
    )


    sku = fields.Char(string='SKU', required=True)
    import_quantity = fields.Integer(string='Số lượng nhập', default=1, required=True)
    export_return_quantity = fields.Integer(string='Số lượng xuất trả', default=0)
    import_price_excl_vat = fields.Float(string='Giá nhập (chưa VAT)', required=True)
    sale_price_incl_vat = fields.Float(string='Giá bán (VAT)', required=True)
    vat_percentage = fields.Float(string='VAT (%)', default=0.0)
    points = fields.Integer(string='Điểm', default=0)
