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


class ReceiptTemplate4Exporter(models.AbstractModel):
    _name = 'receipt.template4.exporter'
    _description = 'Receipt Template 4 Excel Exporter'

    def export_template_4(self, receipt):
        """Export Excel receipt theo mẫu 4"""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet_bbds = workbook.add_worksheet("BBDS")
        worksheet_bk = workbook.add_worksheet("BK")
        worksheet_pt = workbook.add_worksheet("PT")

        # Create BBDS sheet (Biên bản đối soát)
        self._create_bbds_sheet(workbook, worksheet_bbds, receipt)
        
        # Create BK sheet (Bảng kê chi tiết voucher)
        self._create_bk_sheet(workbook, worksheet_bk, receipt)
        
        # Create PT sheet (Phiếu thu)
        self._create_pt_sheet(workbook, worksheet_pt, receipt)

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = f"Phieu_Thu_Mau_4_{receipt.name.replace('/', '_') if receipt.name else 'new'}.xlsx"

        return file_content, filename
        
    def _create_bbds_sheet(self, workbook, worksheet, receipt):
        """Create BBDS sheet (Biên bản đối soát) based on the first image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        subtitle_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10
        })
        cell_bold_format = workbook.add_format({
            'bold': True, 'border': 1, 'valign': 'vcenter', 'font_size': 10
        })
        cell_center_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 'align': 'center'
        })
        cell_right_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 'align': 'right'
        })
        cell_right_red_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 'align': 'right', 'color': 'red'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 5)   # STT
        worksheet.set_column('B:B', 25)  # Nội dung
        worksheet.set_column('C:C', 15)  # Loại Voucher
        worksheet.set_column('D:D', 10)  # Số lượng
        worksheet.set_column('E:E', 15)  # Giá trị
        
        # Title
        worksheet.merge_range('A1:E1', 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM', title_format)
        worksheet.merge_range('A2:E2', 'Độc lập - Tự do - Hạnh phúc', subtitle_format)
        worksheet.merge_range('A3:E3', '***', subtitle_format)
        
        # Report title with month
        month = receipt.receipt_date.strftime('%m/%Y') if receipt.receipt_date else '05/2025'
        worksheet.merge_range('A4:E4', f'BIÊN BẢN ĐỐI SOÁT DỊCH VỤ THÁNG {month}', title_format)
        
        # Time period
        worksheet.merge_range('A5:E5', f'Thời gian từ 00:00:00 01/{month} đến 23:59:59 31/{month}', subtitle_format)
        
        # Company information
        worksheet.merge_range('A7:E7', 'Bên A: CÔNG TY CỔ PHẦN DAYONE', cell_bold_format)
        worksheet.merge_range('A8:E8', 'Bên B: CÔNG TY TNHH DKSH VIỆT NAM', cell_bold_format)
        
        # Contract information
        worksheet.merge_range('A9:E9', 'Căn cứ Hợp đồng dịch vụ số: 1011379/DKSH - DAYONE', cell_format)
        
        # Table headers
        worksheet.write('A11', 'STT', header_format)
        worksheet.write('B11', 'Nội dung', header_format)
        worksheet.write('C11', 'Loại Voucher phát hành', header_format)
        worksheet.write('D11', 'Số Lượng', header_format)
        worksheet.write('E11', 'Giá trị', header_format)
        
        # Data rows
        worksheet.write('A12', '1', cell_center_format)
        worksheet.write('B12', 'Số dư đầu kỳ', cell_format)
        worksheet.write('C12', '', cell_format)
        worksheet.write('D12', '', cell_format)
        worksheet.write('E12', '', cell_format)
        
        worksheet.write('A13', '2', cell_center_format)
        worksheet.write('B13', 'Số tiền thanh toán trong kỳ', cell_format)
        worksheet.write('C13', '', cell_format)
        worksheet.write('D13', '', cell_format)
        worksheet.write('E13', '0', cell_right_format)
        
        # Row 3 with multiple rows merged
        worksheet.write('A14', '3', cell_center_format)
        worksheet.merge_range('A14:A19', '3', cell_center_format)
        worksheet.write('B14', 'Tổng giao dịch thành công', cell_format)
        worksheet.merge_range('B14:B19', 'Tổng giao dịch thành công', cell_format)
        
        # Empty cells for rows 14-19
        for row in range(14, 20):
            worksheet.write(f'C{row}', '', cell_format)
            worksheet.write(f'D{row}', '', cell_format)
            worksheet.write(f'E{row}', '', cell_format)
        
        # Row 4 and 5
        worksheet.write('A20', '4', cell_center_format)
        worksheet.write('B20', 'Tổng phí SMS', cell_format)
        worksheet.write('C20', '', cell_format)
        worksheet.write('D20', '', cell_format)
        worksheet.write('E20', '0', cell_right_format)
        
        worksheet.write('A21', '5', cell_center_format)
        worksheet.write('B21', 'Số dư cuối kỳ', cell_format)
        worksheet.write('C21', '', cell_format)
        worksheet.write('D21', '', cell_format)
        worksheet.write('E21', '0', cell_right_red_format)
        
        # Total
        worksheet.merge_range('A22:D22', 'Tổng số tiền thanh toán dịch vụ Bên B phải thanh toán cho Bên A là:', cell_bold_format)
        worksheet.write('E22', '0', cell_right_format)
        
        # Signatures
        worksheet.merge_range('A24:B24', 'CÔNG TY CỔ PHẦN DAYONE', cell_bold_format)
        worksheet.merge_range('D24:E24', 'CÔNG TY TNHH DKSH VIỆT NAM', cell_bold_format)

    def _create_bk_sheet(self, workbook, worksheet, receipt):
        """Create BK sheet (Bảng kê chi tiết voucher) based on the second image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter',
            'font_size': 10
        })
        
        # Set column widths
        worksheet.set_column('A:A', 4)   # No
        worksheet.set_column('B:B', 15)  # Transaction_refid
        worksheet.set_column('C:C', 12)  # Issue_date
        worksheet.set_column('D:D', 15)  # Campaign_name
        worksheet.set_column('E:E', 15)  # Client_name
        worksheet.set_column('F:F', 15)  # Account_name
        worksheet.set_column('G:G', 15)  # customer_phone
        worksheet.set_column('H:H', 15)  # Product_nam
        worksheet.set_column('I:I', 12)  # Merchant_co
        worksheet.set_column('J:J', 10)  # Price
        worksheet.set_column('K:K', 12)  # Expired_dat
        worksheet.set_column('L:L', 10)  # Status
        
        # Title with month
        month = receipt.receipt_date.strftime('%m/%Y') if receipt.receipt_date else '05/2025'
        worksheet.merge_range('A1:L1', f'BẢNG KÊ CHI TIẾT VOUCHER GOT IT THÁNG {month}', title_format)
        
        # Headers
        worksheet.write('A2', 'No', header_format)
        worksheet.write('B2', 'Transaction_refid', header_format)
        worksheet.write('C2', 'Issue_date', header_format)
        worksheet.write('D2', 'Campaign_name', header_format)
        worksheet.write('E2', 'Client_name', header_format)
        worksheet.write('F2', 'Account_name', header_format)
        worksheet.write('G2', 'customer_phone', header_format)
        worksheet.write('H2', 'Product_nam', header_format)
        worksheet.write('I2', 'Merchant_co', header_format)
        worksheet.write('J2', 'Price', header_format)
        worksheet.write('K2', 'Expired_dat', header_format)
        worksheet.write('L2', 'Status', header_format)
        
        # Create empty rows
        for i in range(1, 25):  # 24 rows as shown in the image
            row = i + 2  # Start from row 3
            worksheet.write(f'A{row}', i, cell_format)
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
                worksheet.write(f'{col}{row}', '', cell_format)
        
        # Total row
        worksheet.merge_range('A27:I27', 'TỔNG CỘNG', total_format)
        for col in ['J', 'K', 'L']:
            worksheet.write(f'{col}27', '', cell_format)

    def _create_pt_sheet(self, workbook, worksheet, receipt):
        """Create PT sheet (Phiếu thu) based on the third image"""
        # Define formats
        company_header_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'valign': 'top', 'font_name': 'Arial'
        })
        receipt_title_format = workbook.add_format({
            'bold': True, 'font_size': 24, 'color': '#FF6600',
            'align': 'right', 'valign': 'top', 'font_name': 'Arial'
        })
        info_format = workbook.add_format({
            'font_size': 11, 'valign': 'top', 'font_name': 'Arial'
        })
        date_format = workbook.add_format({
            'align': 'right', 'font_size': 11, 'valign': 'top', 
            'font_name': 'Arial', 'bg_color': '#FFCC99'
        })
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1, 
            'font_size': 11, 'font_name': 'Arial'
        })
        subheader_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1, 
            'font_size': 11, 'font_name': 'Arial'
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Arial'
        })
        cell_center_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 
            'align': 'center', 'font_name': 'Arial'
        })
        cell_right_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 
            'align': 'right', 'font_name': 'Arial'
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'right', 'valign': 'vcenter',
            'font_size': 10, 'font_name': 'Arial', 'bg_color': '#FFCC99'
        })
        signature_format = workbook.add_format({
            'align': 'center', 'valign': 'top', 'font_size': 10, 
            'bold': True, 'font_name': 'Arial'
        })
        footer_format = workbook.add_format({
            'bold': True, 'italic': True, 'align': 'center',
            'font_size': 12, 'valign': 'vcenter'
        })
        page_number_format = workbook.add_format({
            'font_size': 24, 'color': '#808080', 'align': 'center', 'valign': 'vcenter'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 4)   # STT
        worksheet.set_column('B:B', 30)  # CHI TIÊU
        worksheet.set_column('C:C', 12)  # SỐ LƯỢNG
        worksheet.set_column('D:D', 12)  # ĐƠN GIÁ
        worksheet.set_column('E:E', 8)   # VAT
        worksheet.set_column('F:F', 15)  # THÀNH TIỀN
        
        # Add vertical dotted lines to create the appearance of pages
        # These are visual separators as seen in the image
        worksheet.set_column('C:C', 12, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('F:F', 15, None, {'hidden': False, 'level': 0, 'collapsed': False})
        
        # Company header (left) and Receipt title (right)
        worksheet.merge_range('A1:C1', 'CÔNG TY CỔ PHẦN DAYONE', company_header_format)
        worksheet.merge_range('D1:F1', 'PHIẾU THU', receipt_title_format)
        
        # Company address and info
        worksheet.merge_range('A2:C2', '102 Nguyễn Đình Chiểu, Phường 15, Quận Phú Nhuận', info_format)
        worksheet.merge_range('A3:C3', 'Thành phố Hồ Chí Minh, Việt nam', info_format)
        
        # Date and receipt number
        worksheet.merge_range('D3:F3', '00/.../2025', date_format)
        
        # Tax code
        worksheet.merge_range('A4:C4', 'Mã số thuế/ Tax Code : 0313249098', info_format)
        worksheet.merge_range('D4:F4', '00000000/DO/2025', info_format)
        
        # Bank account
        worksheet.merge_range('A5:F5', 'Tài khoản ngân hàng số : 1081100323005, MB BANK - ĐINH TIẾN HOÀNG', info_format)
        
        # Payer section header
        worksheet.merge_range('A7:F7', 'Người thanh toán', header_format)
        
        # Payer info
        worksheet.merge_range('A8:F8', 'CÔNG TY TNHH DKSH VIỆT NAM', cell_format)
        worksheet.merge_range('A9:F9', 'Số 23 Đại lộ Độc Lập, Khu công nghiệp Việt Nam-Singapore, Phường Bình Hòa, thành phố', cell_format)
        worksheet.merge_range('A10:F10', 'Thuận An, Tỉnh Bình Dương', cell_format)
        worksheet.merge_range('A11:F11', 'Mã số thuế : 3700303206', cell_format)
        
        # Table header with orange background
        worksheet.write('A13', 'CHI TIÊU', header_format)
        worksheet.write('B13', 'SỐ LƯỢNG', header_format)
        worksheet.write('C13', 'ĐƠN GIÁ', header_format)
        worksheet.write('D13', 'VAT', header_format)
        worksheet.write('E13', 'THÀNH TIỀN', header_format)
        worksheet.merge_range('A14:E14', 'THÁNG 05/2025', subheader_format)
        
        # Data rows
        worksheet.write('A15', '1', cell_center_format)
        worksheet.write('B15', 'Voucher Got It Mệnh giá 50.000 VND', cell_format)
        worksheet.write('C15', '', cell_format)
        worksheet.write('D15', '', cell_format)
        worksheet.write('E15', '', cell_format)
        worksheet.write('F15', '-', cell_right_format)
        
        worksheet.write('A16', '2', cell_center_format)
        worksheet.write('B16', 'Voucher Got It Mệnh giá 100.000 VND', cell_format)
        worksheet.write('C16', '', cell_format)
        worksheet.write('D16', '', cell_format)
        worksheet.write('E16', '', cell_format)
        worksheet.write('F16', '-', cell_right_format)
        
        worksheet.write('A17', '3', cell_center_format)
        worksheet.write('B17', 'Voucher Got It Mệnh giá 200.000 VND', cell_format)
        worksheet.write('C17', '', cell_format)
        worksheet.write('D17', '', cell_format)
        worksheet.write('E17', '', cell_format)
        worksheet.write('F17', '-', cell_right_format)
        
        # Total rows
        worksheet.merge_range('A19:E19', 'Tổng số tiền thanh toán', cell_format)
        worksheet.write('F19', '-', cell_right_format)
        
        worksheet.merge_range('A20:E20', '', cell_format)
        worksheet.write('F20', '-', cell_right_format)
        
        worksheet.merge_range('A21:E21', 'Tổng cộng', cell_format)
        worksheet.write('F21', '-', total_format)
        
        # Amount in words
        worksheet.write('A23', 'Bằng chữ :', cell_format)
        worksheet.merge_range('B23:F23', '', cell_format)
        
        # Signature section
        worksheet.merge_range('C26:F26', 'Tên :', signature_format)
        worksheet.merge_range('C27:F27', 'Chức vụ :', signature_format)
        worksheet.merge_range('C28:F28', 'Ký và đóng dấu:', signature_format)
        
        # Footer
        worksheet.merge_range('A35:F35', 'Thank You For Doing Business With GOT IT !', footer_format)