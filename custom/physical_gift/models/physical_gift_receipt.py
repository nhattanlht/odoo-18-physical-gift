# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import io
import base64
from datetime import datetime
try:
    import xlsxwriter  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    xlsxwriter = None


class PhysicalGiftReceipt(models.Model):
    _name = 'physical.gift.receipt'
    _description = 'Physical Gift Receipt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'receipt_date desc'

    name = fields.Char(
        string='Số phiếu thu',
        required=True,
        default='New',
        tracking=True,
        help='Số phiếu thu'
    )

    order_id = fields.Many2one(
        'physical.gift.order',
        string='Đơn hàng',
        required=True,
        tracking=True,
        help='Đơn hàng liên quan'
    )

    receipt_date = fields.Date(
        string='Ngày thu',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help='Ngày lập phiếu thu'
    )

    payer_name = fields.Char(
        string='Người thanh toán',
        required=True,
        tracking=True,
        help='Tên người thanh toán'
    )

    payer_address = fields.Text(
        string='Địa chỉ người thanh toán',
        tracking=True,
        help='Địa chỉ người thanh toán'
    )

    payer_tax_code = fields.Char(
        string='Mã số thuế người thanh toán',
        tracking=True,
        help='Mã số thuế người thanh toán'
    )

    amount = fields.Float(
        string='Số tiền thu',
        required=True,
        tracking=True,
        help='Số tiền thu được'
    )

    amount_in_words = fields.Char(
        string='Số tiền bằng chữ',
        compute='_compute_amount_in_words',
        store=True,
        help='Số tiền viết bằng chữ'
    )

    description = fields.Text(
        string='Diễn giải',
        tracking=True,
        help='Diễn giải nội dung thu'
    )

    payment_method = fields.Selection([
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('credit_card', 'Thẻ tín dụng'),
        ('e_wallet', 'Ví điện tử'),
        ('other', 'Khác')
    ], string='Phương thức thanh toán', default='cash', tracking=True)

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft', tracking=True)

    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        default=lambda self: self.env.company,
        required=True
    )

    @api.depends('amount')
    def _compute_amount_in_words(self):
        for record in self:
            if record.amount:
                # Simplified number to words conversion (Vietnamese)
                record.amount_in_words = self._number_to_words_vn(record.amount)
            else:
                record.amount_in_words = ''

    def _number_to_words_vn(self, number):
        """Convert number to Vietnamese words - simplified version"""
        if number == 0:
            return "Không đồng"
        
        # This is a simplified version - you may want to use a proper library
        # for complete Vietnamese number-to-words conversion
        return f"{number:,.0f} đồng".replace(',', '.')

    def action_confirm(self):
        """Xác nhận phiếu thu"""
        for record in self:
            if record.name == 'New':
                record.name = self.env['ir.sequence'].next_by_code('physical.gift.receipt') or 'PT/001'
            record.state = 'confirmed'

    def action_cancel(self):
        """Hủy phiếu thu"""
        for record in self:
            record.state = 'cancelled'

    def action_reset_to_draft(self):
        """Đưa về trạng thái nháp"""
        for record in self:
            record.state = 'draft'

    def action_export_excel_receipt(self):
        """Export Excel receipt theo mẫu 1 - sử dụng Template Exporter"""
        if not self:
            raise UserError(_("No receipt to export."))

        receipt = self[0]  # Only export single receipt
        
        # Sử dụng Template 1 Exporter
        template1_exporter = self.env['receipt.template1.exporter']
        file_content, filename = template1_exporter.export_template_1(receipt)

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.receipt",
            "res_id": receipt.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }

    def action_export_excel_receipt_template_2(self):
        """Export Excel receipt theo mẫu 2 - sử dụng Template Exporter"""
        if not self:
            raise UserError(_("No receipt to export."))

        receipt = self[0]  # Only export single receipt
        
        # Sử dụng Template 2 Exporter
        template2_exporter = self.env['receipt.template2.exporter']
        file_content, filename = template2_exporter.export_template_2(receipt)

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.receipt",
            "res_id": receipt.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }

    def action_export_excel_receipt_template_3(self):
        """Export Excel receipt theo mẫu 3 - sử dụng Template Exporter"""
        if not self:
            raise UserError(_("No receipt to export."))

        receipt = self[0]  # Only export single receipt
        
        # Sử dụng Template 3 Exporter
        template3_exporter = self.env['receipt.template3.exporter']
        file_content, filename = template3_exporter.export_template_3(receipt)

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.receipt",
            "res_id": receipt.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }

    def action_export_excel_receipt_template_4(self):
        """Export Excel receipt theo mẫu 4 - sử dụng Template Exporter"""
        if not self:
            raise UserError(_("No receipt to export."))

        receipt = self[0]  # Only export single receipt
        
        # Sử dụng Template 4 Exporter
        template4_exporter = self.env['receipt.template4.exporter']
        file_content, filename = template4_exporter.export_template_4(receipt)

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.receipt",
            "res_id": receipt.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }

    def action_export_excel_receipt_template_5(self):
        """Export Excel receipt theo mẫu 5 - sử dụng Template Exporter"""
        if not self:
            raise UserError(_("No receipt to export."))

        receipt = self[0]  # Only export single receipt
        
        # Sử dụng Template 5 Exporter
        template5_exporter = self.env['receipt.template5.exporter']
        file_content, filename = template5_exporter.export_template_5(receipt)

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.receipt",
            "res_id": receipt.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} - {record.payer_name}"
            result.append((record.id, name))
        return result