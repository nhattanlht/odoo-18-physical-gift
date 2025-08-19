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


class ReceiptTemplate1Exporter(models.AbstractModel):
    _name = 'receipt.template1.exporter'
    _description = 'Receipt Template 1 Excel Exporter'

    def export_template_1(self, receipt):
        """Export Excel receipt theo mẫu 1 - DayOne Style"""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Phiếu Thu")
        worksheet_bk_phi_dv = workbook.add_worksheet("BK PHÍ DV")
        worksheet_bang_ke = workbook.add_worksheet("BANG KE-in")

        # Define formats
        company_header_format = workbook.add_format({
            'bold': True, 'font_size': 18, 'valign': 'top', 'font_name': 'Trebuchet MS'
        })
        receipt_title_format = workbook.add_format({
            'bold': True, 'font_size': 26, 'color': '#FF6600',
            'align': 'right', 'valign': 'top', 'font_name': 'Trebuchet MS'
        })
        date_format = workbook.add_format({
            'align': 'right', 'font_size': 11,
            'bg_color': '#FFE4B5'
        })
        payer_header_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'left', 'valign': 'vcenter', 'border': 1, 'font_size': 11, 'font_name': 'Trebuchet MS'
        })
        table_header_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1, 'font_size': 11, 'font_name': 'Trebuchet MS'
        })
        table_cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter'
        })
        table_number_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0'
        })
        total_format = workbook.add_format({
            'bold': True, 'bg_color': '#FFE4B5',
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0'
        })
        signature_format = workbook.add_format({
            'align': 'center', 'valign': 'top', 'font_size': 10, 'bold': True
        })
        footer_format = workbook.add_format({
            'bold': True, 'italic': True, 'align': 'center',
            'font_size': 12, 'valign': 'vcenter'
        })

        # Set column widths
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 15)

        # Company header (left) and Receipt title (right)
        worksheet.merge_range('A1:C1', receipt.company_id.name or 'CÔNG TY CỔ PHẦN DAYONE', company_header_format)
        worksheet.write('F1', 'PHIẾU THU', receipt_title_format)
        
        worksheet.merge_range(
            'A2:E2',
            receipt.company_id.street or 'Tòa nhà 9-11 Nguyễn Văn Thủ, P. Đa Kao, Q.1',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.merge_range('A3:D3', receipt.company_id.city or 'Thành phố Hồ Chí Minh, Việt nam',
            workbook.add_format({'font_size': 12, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.write('F3', receipt.receipt_date.strftime('%d/%m/%Y'), date_format)
        
        worksheet.merge_range('A4:D4', f'Mã số thuế/Tax Code : {receipt.company_id.vat or "0313249098"}',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.write('F4', receipt.name or '00000000/DO/2025', 
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )
        
        # Bank account info
        worksheet.merge_range('A5:E5', 'Tài khoản ngân hàng số : 191.3341.5336.013, TECHCOMBANK, CN SÀI GÒN',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        # Payer section
        worksheet.merge_range('A7:D7', 'Người thanh toán', payer_header_format)
        worksheet.write('A8', receipt.payer_name or '[COMPANY_NAME]', table_cell_format)
        worksheet.write('A9', receipt.payer_address or '[COMPANY_ADDRESS]', table_cell_format)
        worksheet.write('A10', f'Mã số thuế : {receipt.payer_tax_code or "[COMPANY_TAX_CODE]"}', table_cell_format)

        # Table header
        worksheet.write('A12', 'CHI TIẾT', table_header_format)
        worksheet.write('B12', f'THÁNG {receipt.receipt_date.month}/{receipt.receipt_date.year}', table_header_format)
        worksheet.write('C12', 'SỐ LƯỢNG', table_header_format)
        worksheet.write('D12', 'ĐƠN GIÁ', table_header_format)
        worksheet.write('E12', 'VAT', table_header_format)
        worksheet.write('F12', 'THÀNH TIỀN', table_header_format)

        # Data rows
        row = 13
        worksheet.write(f'A{row}', '[NO]', table_cell_format)
        worksheet.write(f'B{row}', receipt.description or '[VOUCHER_BY_PRICE]', table_cell_format)
        worksheet.write(f'C{row}', '1', table_cell_format)
        worksheet.write(f'D{row}', receipt.amount, table_number_format)
        worksheet.write(f'E{row}', '', table_cell_format)
        worksheet.write(f'F{row}', receipt.amount, table_number_format)

        # Total rows
        worksheet.merge_range(f'A{row+2}:E{row+2}', 'Tổng số tiền thanh toán', table_cell_format)
        worksheet.write(f'F{row+2}', receipt.amount, total_format)

        worksheet.merge_range(f'A{row+3}:E{row+3}', '', table_cell_format)
        worksheet.write(f'F{row+3}', '-', table_cell_format)

        worksheet.merge_range(f'A{row+4}:E{row+4}', '', table_cell_format)
        worksheet.write(f'F{row+4}', '-', table_cell_format)

        worksheet.merge_range(f'A{row+5}:E{row+5}', 'Tổng cộng', table_cell_format)
        worksheet.write(f'F{row+5}', receipt.amount, total_format)

        # Amount in words
        worksheet.write(f'A{row+7}', 'Bằng chữ :', table_cell_format)
        worksheet.merge_range(f'B{row+7}:F{row+7}', receipt.amount_in_words, table_cell_format)

        # Signature section
        sig_row = row + 15
        worksheet.write(f'D{sig_row}', 'Tên :', signature_format)
        worksheet.write(f'D{sig_row+1}', 'Chức vụ :', signature_format)
        worksheet.write(f'D{sig_row+2}', 'Ký và đóng dấu:', signature_format)

        # Footer
        footer_row = sig_row + 10
        worksheet.merge_range(f'A{footer_row}:F{footer_row}', 'Thank You For Doing Business With GOT IT !', footer_format)

        # === SHEET 2: BK PHÍ DV ===
        self._create_bk_phi_dv_sheet(workbook, worksheet_bk_phi_dv, receipt)

        # === SHEET 3: BANG KE-in ===
        self._create_bang_ke_sheet(workbook, worksheet_bang_ke, receipt)

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = f"(C) DOI SOAT BRAVOHR.xlsx"

        return file_content, filename

    def _create_bk_phi_dv_sheet(self, workbook, worksheet, receipt):
        """Tạo sheet BK PHÍ DV theo mẫu"""
        # Define formats for BK PHÍ DV
        title_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10, 'text_wrap': True
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9
        })
        number_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0', 'font_size': 9
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0', 'font_size': 9
        })

        # Set column widths
        worksheet.set_column('A:A', 4)   # N
        worksheet.set_column('B:B', 15)  # Issue_date
        worksheet.set_column('C:C', 20)  # Campaign_name
        worksheet.set_column('D:D', 20)  # Company_name
        worksheet.set_column('E:E', 18)  # Account_name
        worksheet.set_column('F:F', 12)  # Price
        worksheet.set_column('G:G', 12)  # Expired_r
        worksheet.set_column('H:H', 20)  # Ref_id
        worksheet.set_column('I:I', 18)  # Product_nar
        worksheet.set_column('J:J', 15)  # Merchant_c

        # Title
        worksheet.merge_range('A2:L2', 'BẢNG KÊ CHI TIẾT (Xăng dầu / Nạp tiền điện thoại trực tiếp / Mã thẻ nạp điện thoại)', title_format)

        # Headers row 1
        worksheet.write('A5', 'N', header_format)
        worksheet.write('B5', 'Issue_date', header_format)
        worksheet.write('C5', 'Campaign_name', header_format)
        worksheet.write('D5', 'Company_name', header_format)
        worksheet.write('E5', 'Account_name', header_format)
        worksheet.write('F5', 'Price', header_format)
        worksheet.write('G5', 'Expired_r', header_format)
        worksheet.write('H5', 'Ref_id', header_format)
        worksheet.write('I5', 'Product_nar', header_format)
        worksheet.write('J5', 'Merchant_c', header_format)

        # Sample data rows
        worksheet.write('A7', '[NO]', cell_format)
        worksheet.write('B7', '[VOUCHER_ISSUED_TIME]', cell_format)
        worksheet.write('C7', '[ORDER_NAME]', cell_format)
        worksheet.write('D7', '[COMPANY_NAME]', cell_format)
        worksheet.write('E7', '[ACCOUNT_NAME]', cell_format)
        worksheet.write('F7', '[VOUCHER_VALUE]', number_format)
        worksheet.write('G7', '[VOUCHER_TRANSACTION_REFID]', cell_format)
        worksheet.write('H7', '[PRODUCT_NAME]', cell_format)
        worksheet.write('I7', '[PRODUCT_BRAND]', cell_format)

        worksheet.write('A8', '[NO]', cell_format)
        worksheet.write('B8', '[VOUCHER_ISSUED_TIME]', cell_format)
        worksheet.write('C8', '[ORDER_NAME]', cell_format)
        worksheet.write('D8', '[COMPANY_NAME]', cell_format)
        worksheet.write('E8', '[ACCOUNT_NAME]', cell_format)
        worksheet.write('F8', '[VOUCHER_VALUE]', number_format)
        worksheet.write('G8', '[VOUCHER_TRANSACTION_REFID]', cell_format)
        worksheet.write('H8', '[PRODUCT_NAME]', cell_format)
        worksheet.write('I8', '[PRODUCT_BRAND]', cell_format)

        # Total rows
        worksheet.merge_range('A10:E10', 'TỔNG', header_format)
        worksheet.write('F10', '-', total_format)
        worksheet.merge_range('A11:E11', '% PHÍ DỊCH VỤ', header_format)
        worksheet.write('F11', '-', total_format)
        worksheet.merge_range('A12:E12', 'PHÍ DỊCH VỤ', header_format)
        worksheet.write('F12', '-', total_format)

    def _create_bang_ke_sheet(self, workbook, worksheet, receipt):
        """Tạo sheet BANG KE-in theo mẫu"""
        # Define formats for BANG KE-in
        title_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10, 'text_wrap': True
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9
        })
        number_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0', 'font_size': 9
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'right', 'valign': 'vcenter',
            'num_format': '#,##0', 'font_size': 9
        })

        # Set column widths
        worksheet.set_column('A:A', 4)   # N
        worksheet.set_column('B:B', 15)  # Issue_date
        worksheet.set_column('C:C', 20)  # Campaign_name
        worksheet.set_column('D:D', 20)  # Company_name
        worksheet.set_column('E:E', 18)  # Account_name
        worksheet.set_column('F:F', 12)  # Customer_id
        worksheet.set_column('G:G', 12)  # Customer_name
        worksheet.set_column('H:H', 15)  # Customer_email
        worksheet.set_column('I:I', 18)  # Product_name
        worksheet.set_column('J:J', 15)  # Merchant_c
        worksheet.set_column('K:K', 12)  # Price
        worksheet.set_column('L:L', 12)  # Expired_r
        worksheet.set_column('M:M', 20)  # Ref_id

        # Title
        worksheet.merge_range('A2:O2', 'BẢNG KÊ CHI TIẾT VOUCHER GOT IT', title_format)

        # Headers
        worksheet.write('A5', 'N', header_format)
        worksheet.write('B5', 'Issue_date', header_format)
        worksheet.write('C5', 'Campaign_name', header_format)
        worksheet.write('D5', 'Company_name', header_format)
        worksheet.write('E5', 'Account_na', header_format)
        worksheet.write('F5', 'Customer_i', header_format)
        worksheet.write('G5', 'Customer_na', header_format)
        worksheet.write('H5', 'Customer_em', header_format)
        worksheet.write('I5', 'Product_name', header_format)
        worksheet.write('J5', 'Merchant_c', header_format)
        worksheet.write('K5', 'Price', header_format)
        worksheet.write('L5', 'Expired_r', header_format)
        worksheet.write('M5', 'Ref_id', header_format)

        # Sample data rows
        worksheet.write('A7', '[NO]', cell_format)
        worksheet.write('B7', '[VOUCHER_ISSUED_TIME]', cell_format)
        worksheet.write('C7', '[ORDER_NAME]', cell_format)
        worksheet.write('D7', '[COMPANY_NAME]', cell_format)
        worksheet.write('E7', '[ACCOUNT_NAME]', cell_format)
        worksheet.write('F7', '[VOUCHER_CUSTOMER_NAME]', cell_format)
        worksheet.write('G7', '[VOUCHER_CUSTOMER_NAME]', cell_format)
        worksheet.write('H7', '[VOUCHER_CUSTOMER_EMAIL]', cell_format)
        worksheet.write('I7', '[PRODUCT_NAME]', cell_format)
        worksheet.write('J7', '[PRODUCT_BRAND]', cell_format)
        worksheet.write('K7', '[VOUCHER_VALUE]', number_format)
        worksheet.write('L7', '[VOUCHER_EXPIRED_TIME]', cell_format)
        worksheet.write('M7', '[VOUCHER_TRANSACTION_REFID]', cell_format)

        worksheet.write('A8', '[NO]', cell_format)
        worksheet.write('B8', '[VOUCHER_ISSUED_TIME]', cell_format)
        worksheet.write('C8', '[ORDER_NAME]', cell_format)
        worksheet.write('D8', '[COMPANY_NAME]', cell_format)
        worksheet.write('E8', '[ACCOUNT_NAME]', cell_format)
        worksheet.write('F8', '[VOUCHER_CUSTOMER_NAME]', cell_format)
        worksheet.write('G8', '[VOUCHER_CUSTOMER_NAME]', cell_format)
        worksheet.write('H8', '[VOUCHER_CUSTOMER_EMAIL]', cell_format)
        worksheet.write('I8', '[PRODUCT_NAME]', cell_format)
        worksheet.write('J8', '[PRODUCT_BRAND]', cell_format)
        worksheet.write('K8', '[VOUCHER_VALUE]', number_format)
        worksheet.write('L8', '[VOUCHER_EXPIRED_TIME]', cell_format)
        worksheet.write('M8', '[VOUCHER_TRANSACTION_REFID]', cell_format)

        # Total row
        worksheet.merge_range('A10:J10', 'TỔNG CỘNG', header_format)
        worksheet.write('K10', '-', total_format)