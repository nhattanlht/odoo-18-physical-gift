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


class PhysicalGiftOrder(models.Model):
    _name = 'physical.gift.order'
    _description = 'Physical Gift Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Mã đơn hàng',
        required=True,
        default='New',
        tracking=True,
        help='Mã đơn hàng'
    )

    program_id = fields.Many2one(
        'physical.gift.program',
        string='Chương trình',
        required=True,
        tracking=True,
        domain=[('active', '=', True)],
        help='Chương trình liên quan'
    )

    recipient_name = fields.Char(
        string='Tên người nhận',
        required=True,
        tracking=True,
        help='Tên người nhận hàng'
    )

    recipient_phone = fields.Char(
        string='Số điện thoại người nhận',
        required=True,
        tracking=True,
        help='Số điện thoại người nhận'
    )

    total_order_value = fields.Float(
        string='Tổng giá trị đơn hàng',
        required=True,
        tracking=True,
        help='Tổng giá trị đơn hàng'
    )

    voucher_code = fields.Char(
        string='Mã voucher',
        tracking=True,
        help='Mã voucher'
    )

    shipping_unit_id = fields.Many2one(
        'physical.gift.shipping.unit',
        string='Đơn vị vận chuyển',
        tracking=True,
        domain=[('state', '=', 'active')],
        help='Đơn vị vận chuyển'
    )

    waybill_code = fields.Char(
        string='Mã vận đơn',
        tracking=True,
        help='Mã vận đơn'
    )

    payment_gateway = fields.Selection([
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('cash', 'Tiền mặt'),
        ('credit_card', 'Thẻ tín dụng'),
        ('e_wallet', 'Ví điện tử'),
        ('other', 'Khác')
    ], string='Cổng thanh toán', tracking=True)

    payment_status = fields.Selection([
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền')
    ], string='Trạng thái thanh toán', default='pending', tracking=True)

    transaction_code = fields.Char(
        string='Mã giao dịch',
        tracking=True,
        help='Mã giao dịch thanh toán'
    )

    product_type = fields.Selection([
        ('physical', 'Sản phẩm vật lý'),
        ('digital', 'Sản phẩm số'),
        ('service', 'Dịch vụ'),
        ('other', 'Khác')
    ], string='Loại sản phẩm', default='physical', tracking=True)

    order_time = fields.Datetime(
        string='Thời gian đặt hàng',
        required=True,
        default=fields.Datetime.now,
        tracking=True,
        help='Thời gian đặt hàng'
    )

    create_date = fields.Datetime(
        string='Thời gian tạo',
        default=fields.Datetime.now,
        tracking=True,
        help='Thời gian tạo đơn hàng'
    )

    order_status = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('returned', 'Đã trả hàng')
    ], string='Trạng thái đơn hàng', default='draft', tracking=True)

    error_content = fields.Text(
        string='Nội dung lỗi',
        tracking=True,
        help='Nội dung lỗi nếu có'
    )

    notes = fields.Text(
        string='Ghi chú',
        tracking=True,
        help='Ghi chú về đơn hàng'
    )

    # Danh sách sản phẩm trong đơn
    order_line_ids = fields.One2many(
        'physical.gift.order.line',
        'order_id',
        string='Danh sách sản phẩm',
        tracking=True
    )

    # Actions
    def action_confirm(self):
        """Xác nhận đơn hàng và trừ tồn kho"""
        for order in self:
            if not order.order_line_ids:
                raise UserError(_("Đơn hàng phải có ít nhất một sản phẩm."))

            # Kiểm tra tồn kho đủ không
            for line in order.order_line_ids:
                if line.item_id.quantity < line.quantity:
                    raise UserError(
                        _("Sản phẩm '%s' không đủ tồn kho (còn %s, yêu cầu %s).")
                        % (line.item_id.name, line.item_id.quantity, line.quantity)
                    )

            # Trừ tồn kho
            for line in order.order_line_ids:
                line.item_id.sudo().write({
                    'quantity': line.item_id.quantity - line.quantity
                })

            order.order_status = 'confirmed'

    def action_process(self):
        for record in self:
            record.order_status = 'processing'

    def action_ship(self):
        for record in self:
            record.order_status = 'shipped'

    def action_cancel(self):
        for record in self:
            record.order_status = 'cancelled'

    def action_return(self):
        for record in self:
            record.order_status = 'returned'

    def action_reset_to_draft(self):
        for record in self:
            record.order_status = 'draft'

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} - {record.recipient_name}"
            result.append((record.id, name))
        return result

    def action_export_excel(self):
        """Generate a formatted Excel file for selected orders and return a download action."""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        orders = self
        if not orders:
            raise UserError(_("No orders to export."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Orders")

        # Formats
        title_format = workbook.add_format({
            "bold": True, "font_size": 14, "align": "center", "valign": "vcenter"
        })
        header_format = workbook.add_format({
            "bold": True, "font_color": "white", "bg_color": "#4472C4",
            "border": 1, "align": "center", "valign": "vcenter"
        })
        text_format = workbook.add_format({"border": 1, "valign": "vcenter"})
        center_format = workbook.add_format({"border": 1, "align": "center", "valign": "vcenter"})
        number_format = workbook.add_format({"border": 1, "align": "right", "valign": "vcenter", "num_format": "#,##0.00"})

        # Column settings
        columns = [
            ("Mã đơn", 15),
            ("Chương trình", 25),
            ("Người nhận", 20),
            ("SĐT", 15),
            ("Tổng tiền", 15),
            ("Trạng thái", 15),
            ("Ngày đặt", 20),
        ]
        for idx, (_, width) in enumerate(columns):
            worksheet.set_column(idx, idx, width)

        # Title (merged)
        worksheet.merge_range(0, 0, 0, len(columns) - 1, "Physical Gift Orders", title_format)

        # Header row
        header_row = 1
        for col, (title, _) in enumerate(columns):
            worksheet.write(header_row, col, title, header_format)

        # Selection labels for status
        status_selection = dict(self._fields["order_status"].selection)

        # Data rows
        row = header_row + 1
        for order in orders:
            worksheet.write(row, 0, order.name or "", center_format)
            worksheet.write(row, 1, order.program_id.display_name or "", text_format)
            worksheet.write(row, 2, order.recipient_name or "", text_format)
            worksheet.write(row, 3, order.recipient_phone or "", text_format)
            worksheet.write_number(row, 4, float(order.total_order_value or 0.0), number_format)
            worksheet.write(row, 5, status_selection.get(order.order_status, order.order_status or ""), center_format)
            # Format datetime to string for clarity
            order_time_str = ""
            if order.order_time:
                # Convert to user timezone string
                dt = fields.Datetime.context_timestamp(self, order.order_time)
                order_time_str = dt.strftime("%Y-%m-%d %H:%M:%S") if isinstance(dt, datetime) else str(dt)
            worksheet.write(row, 6, order_time_str, center_format)
            row += 1

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = "Physical_Gift_Orders_%s.xlsx" % fields.Datetime.now().strftime("%Y%m%d_%H%M%S")

        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": file_content,
            "res_model": "physical.gift.order",
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=1",
            "target": "self",
        }


class PhysicalGiftOrderLine(models.Model):
    _name = 'physical.gift.order.line'
    _description = 'Dòng sản phẩm đơn hàng'

    order_id = fields.Many2one(
        'physical.gift.order',
        string='Đơn hàng',
        required=True,
        ondelete='cascade'
    )

    item_id = fields.Many2one(
        'physical.gift.item',
        string='Sản phẩm',
        required=True,
        domain=[('active', '=', True)]
    )

    quantity = fields.Integer(
        string='Số lượng',
        required=True,
        default=1
    )

    unit_price = fields.Float(
        string='Đơn giá',
    )

    total_price = fields.Float(
        string='Thành tiền',
        compute='_compute_total_price',
        store=True
    )

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.unit_price
