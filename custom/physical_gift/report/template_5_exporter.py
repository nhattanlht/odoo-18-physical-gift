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


class ReceiptTemplate5Exporter(models.AbstractModel):
    _name = 'receipt.template5.exporter'
    _description = 'Receipt Template 5 Excel Exporter'

    def export_template_5(self, receipt):
        """Export Excel receipt theo mẫu 5"""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet_pt = workbook.add_worksheet("PT")
        worksheet_bk = workbook.add_worksheet("BK")
        worksheet_bbds = workbook.add_worksheet("BBDS")
        worksheet_chuyen = workbook.add_worksheet("chuyen sang thang sau")

        # Create PT sheet (Phiếu thu - Seabank version)
        self._create_pt_sheet(workbook, worksheet_pt, receipt)
        
        # Create BK sheet (Bảng kê chi tiết voucher)
        self._create_bk_sheet(workbook, worksheet_bk, receipt)
        
        # Create BBDS sheet (Biên bản đối soát chi tiết)
        self._create_bbds_sheet(workbook, worksheet_bbds, receipt)
        
        # Create chuyen sang thang sau sheet
        self._create_chuyen_sang_thang_sau_sheet(workbook, worksheet_chuyen, receipt)

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = f"Phieu_Thu_Mau_5_{receipt.name.replace('/', '_') if receipt.name else 'new'}.xlsx"

        return file_content, filename
        
    def _create_pt_sheet(self, workbook, worksheet, receipt):
        """Create PT sheet (Phiếu thu - Seabank version) based on the first image"""
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
        payer_header_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'left', 'valign': 'vcenter', 'border': 1, 
            'font_size': 11, 'font_name': 'Arial'
        })
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'center', 'valign': 'vcenter', 'border': 1, 
            'font_size': 11, 'font_name': 'Arial'
        })
        subheader_format = workbook.add_format({
            'bold': True, 'bg_color': '#FF6600', 'font_color': 'white',
            'align': 'left', 'valign': 'vcenter', 'border': 1, 
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
            'align': 'left', 'valign': 'top', 'font_size': 10, 
            'bold': True, 'font_name': 'Arial'
        })
        footer_format = workbook.add_format({
            'bold': True, 'italic': True, 'align': 'center',
            'font_size': 12, 'valign': 'vcenter'
        })
        
        # Set exact column widths to match the image layout
        worksheet.set_column('A:A', 8)   # CHI TIÊU (wider as shown)
        worksheet.set_column('B:B', 30)  # Voucher descriptions (much wider)
        worksheet.set_column('C:C', 12)  # SỐ LƯỢNG
        worksheet.set_column('D:D', 12)  # ĐƠN GIÁ
        worksheet.set_column('E:E', 8)   # VAT
        worksheet.set_column('F:F', 15)  # THÀNH TIỀN
        
        # Company header (left) and Receipt title (right) - as shown in image
        worksheet.merge_range('A1:D1', 'CÔNG TY CỔ PHẦN DAYONE', company_header_format)
        worksheet.merge_range('E1:F1', 'PHIẾU THU', receipt_title_format)
        
        # Company address and info
        worksheet.merge_range('A2:D2', '102 Nguyễn Đình Chiểu, Phường 15, Quận Phú Nhuận', info_format)
        worksheet.merge_range('A3:D3', 'Thành phố Hồ Chí Minh, Việt nam', info_format)
        
        # Date and receipt number - in orange boxes as shown
        worksheet.merge_range('E2:F2', '00/.../2025', date_format)
        worksheet.merge_range('E3:F3', '00000000/DO/2025', date_format)
        
        # Tax code
        worksheet.merge_range('A4:D4', 'Mã số thuế/ Tax Code : 0313249098', info_format)
        
        # Bank account
        worksheet.merge_range('A5:F5', 'Tài khoản ngân hàng số : 191.3341.5336.013, TECHCOMBANK, CN SÀI GÒN', info_format)
        
        # Payer section header - full width orange background
        worksheet.merge_range('A7:F7', 'Người thanh toán', payer_header_format)
        
        # Payer info (Seabank version) - full width
        worksheet.merge_range('A8:F8', 'NGÂN HÀNG TMCP ĐÔNG NAM Á (SEABANK)', cell_format)
        worksheet.merge_range('A9:F9', '25 Trần Hưng Đạo, Phường Phan Chu Trinh, Quận Hoàn Kiếm, TP. Hà Nội, Việt Nam', cell_format)
        worksheet.merge_range('A10:F10', 'Mã số thuế : 0200253985', cell_format)
        
        # Table header with orange background - exact layout from image
        worksheet.write('A12', 'CHI TIÊU', header_format)
        worksheet.write('B12', 'SỐ LƯỢNG', header_format)
        worksheet.write('C12', 'ĐƠN GIÁ', header_format)
        worksheet.write('D12', 'VAT', header_format)
        worksheet.write('E12', 'THÀNH TIỀN', header_format)
        
        # Month subheader - spans first column and is left-aligned
        worksheet.write('A13', 'THÁNG 05/2025', subheader_format)
        for col in ['B', 'C', 'D', 'E']:
            worksheet.write(f'{col}13', '', subheader_format)
        
        # Data rows - exactly as shown in image with proper column placement
        worksheet.write('A14', '1', cell_center_format)
        worksheet.write('B14', 'Voucher Got It Mệnh giá 10.000 VND', cell_format)
        worksheet.write('C14', '', cell_format)
        worksheet.write('D14', '', cell_format)
        worksheet.write('E14', '', cell_format)
        worksheet.write('F14', '-', cell_right_format)
        
        worksheet.write('A15', '2', cell_center_format)
        worksheet.write('B15', 'Voucher Got It Mệnh giá 20.000 VND', cell_format)
        worksheet.write('C15', '', cell_format)
        worksheet.write('D15', '', cell_format)
        worksheet.write('E15', '', cell_format)
        worksheet.write('F15', '-', cell_right_format)
        
        worksheet.write('A16', '3', cell_center_format)
        worksheet.write('B16', 'Voucher Got It Mệnh giá 50.000 VND', cell_format)
        worksheet.write('C16', '', cell_format)
        worksheet.write('D16', '', cell_format)
        worksheet.write('E16', '', cell_format)
        worksheet.write('F16', '-', cell_right_format)
        
        worksheet.write('A17', '4', cell_center_format)
        worksheet.write('B17', 'Voucher Got It Mệnh giá 100.000 VND', cell_format)
        worksheet.write('C17', '', cell_format)
        worksheet.write('D17', '', cell_format)
        worksheet.write('E17', '', cell_format)
        worksheet.write('F17', '-', cell_right_format)
        
        worksheet.write('A18', '5', cell_center_format)
        worksheet.write('B18', 'Voucher Got It Mệnh giá 200.000 VND', cell_format)
        worksheet.write('C18', '', cell_format)
        worksheet.write('D18', '', cell_format)
        worksheet.write('E18', '', cell_format)
        worksheet.write('F18', '-', cell_right_format)
        
        # Total rows - positioned as in the image (right side)
        worksheet.merge_range('D20:E20', 'Tổng số tiền thanh toán', cell_format)
        worksheet.write('F20', '-', cell_right_format)
        
        worksheet.merge_range('D21:E21', '', cell_format)
        worksheet.write('F21', '-', cell_right_format)
        
        worksheet.merge_range('D22:E22', 'Tổng cộng', cell_format)
        worksheet.write('F22', '-', total_format)
        
        # Amount in words - left side as shown
        worksheet.write('A24', 'Bằng chữ :', cell_format)
        
        # Signature section - positioned on the right as in image
        worksheet.merge_range('D27:F27', 'Tên :', signature_format)
        worksheet.merge_range('D28:F28', 'Chức vụ :', signature_format)
        worksheet.merge_range('D29:F29', 'Ký và đóng dấu:', signature_format)
        
        # Footer
        worksheet.merge_range('A36:F36', 'Thank You For Doing Business With GOT IT !', footer_format)

    def _create_bk_sheet(self, workbook, worksheet, receipt):
        """Create BK sheet (Bảng kê chi tiết voucher) based on the second image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 8
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter',
            'font_size': 9
        })
        
        # Set column widths for all columns (based on the image)
        worksheet.set_column('A:A', 4)   # No
        worksheet.set_column('B:B', 12)  # Transaction_refid
        worksheet.set_column('C:C', 10)  # Issue_date
        worksheet.set_column('D:D', 12)  # Campaign_name
        worksheet.set_column('E:E', 12)  # Client_name
        worksheet.set_column('F:F', 12)  # Account_name
        worksheet.set_column('G:G', 12)  # Customer_name
        worksheet.set_column('H:H', 12)  # Customer_phone
        worksheet.set_column('I:I', 12)  # Product_name
        worksheet.set_column('J:J', 10)  # Merchant_code
        worksheet.set_column('K:K', 8)   # Price
        worksheet.set_column('L:L', 10)  # Expired_date
        worksheet.set_column('M:M', 8)   # Status
        worksheet.set_column('N:N', 10)  # category_brand
        
        # Title with month
        month = receipt.receipt_date.strftime('%m/%Y') if receipt.receipt_date else '05/2025'
        worksheet.merge_range('A1:N1', f'BẢNG KÊ CHI TIẾT VOUCHER GOT IT THÁNG {month}', title_format)
        
        # Headers
        worksheet.write('A2', 'No', header_format)
        worksheet.write('B2', 'Transaction_refid', header_format)
        worksheet.write('C2', 'Issue_date', header_format)
        worksheet.write('D2', 'Campaign_name', header_format)
        worksheet.write('E2', 'Client_name', header_format)
        worksheet.write('F2', 'Account_name', header_format)
        worksheet.write('G2', 'Customer_name', header_format)
        worksheet.write('H2', 'Customer_phone', header_format)
        worksheet.write('I2', 'Product_name', header_format)
        worksheet.write('J2', 'Merchant_code', header_format)
        worksheet.write('K2', 'Price', header_format)
        worksheet.write('L2', 'Expired_date', header_format)
        worksheet.write('M2', 'Status', header_format)
        worksheet.write('N2', 'category_brand', header_format)
        
        # Create empty rows
        for i in range(1, 30):  # 29 rows as shown in the image
            row = i + 2  # Start from row 3
            worksheet.write(f'A{row}', i, cell_format)
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']:
                worksheet.write(f'{col}{row}', '', cell_format)
        
        # Total row
        worksheet.merge_range('A32:K32', 'TỔNG CỘNG', total_format)
        worksheet.write('L32', '-', cell_format)
        worksheet.write('M32', '', cell_format)
        worksheet.write('N32', '', cell_format)

    def _create_bbds_sheet(self, workbook, worksheet, receipt):
        """Create BBDS sheet based on the detailed reconciliation report image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter',
            'font_size': 12, 'text_wrap': True
        })
        subtitle_format = workbook.add_format({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 9, 'text_wrap': True
        })
        section_header_format = workbook.add_format({
            'bold': True, 'font_size': 10, 'text_wrap': True
        })
        red_text_format = workbook.add_format({
            'font_size': 9, 'text_wrap': True, 'color': 'red'
        })
        red_text_center_format = workbook.add_format({
            'font_size': 9, 'text_wrap': True, 'color': 'red', 'align': 'center'
        })
        red_section_format = workbook.add_format({
            'bold': True, 'font_size': 10, 'text_wrap': True, 'color': 'red'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9, 'text_wrap': True, 'bg_color': '#D9D9D9'
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9, 'text_wrap': True
        })
        cell_center_format = workbook.add_format({
            'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9
        })
        cell_right_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter', 'font_size': 9
        })
        signature_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter',
            'font_size': 10
        })
        
        # Set column widths to match the detailed layout
        worksheet.set_column('A:A', 35)  # Nhóm ngành - wider for descriptions
        worksheet.set_column('B:B', 12)  # Số lượng
        worksheet.set_column('C:C', 15)  # Tổng tiền (VNĐ)
        worksheet.set_column('D:D', 15)  # Additional columns for complex table
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 15)
        
        # Title and subtitle
        worksheet.merge_range('A1:H1', 'BIÊN BẢN XÁC NHẬN SỐ LIỆU GIAO DỊCH THU HỘ, PHÍ THU HỘ', title_format)
        worksheet.merge_range('A2:H2', 'GIAO DỊCH THU HỘ SAI LỆCH, PHÍ THU HỘ SAI LỆCH', title_format)
        
        # Contract and period info
        worksheet.merge_range('A3:H3', '(Đính kèm Phụ lục 01 - Chính sách phí thu hộ, điều khoản thanh toán và quy trình dịch vụ)', subtitle_format)
        worksheet.merge_range('A4:H4', 'Kỳ lập phí từ ngày 01/05/2025 đến ngày 31/05/2025', red_text_center_format)
        
        # Agreement details
        worksheet.merge_range('A5:H5', 'Căn cứ Hợp đồng cung cấp dịch vụ thu hộ số: B2B/2022/HĐNT/DAYONE - SEABANK giữa Ngân hàng TMCP Đông Nam Á (SeABank) và Công ty Cổ Phần', cell_format)
        worksheet.merge_range('A6:H6', 'Căn cứ vào Phụ lục số 01 - Chính sách phí thu hộ, điều khoản thanh toán và quy trình dịch vụ,', cell_format)
        worksheet.merge_range('A7:H7', 'Hôm nay, ngày     tháng     năm 2025', cell_format)
        worksheet.merge_range('A8:H8', 'Hai bên cùng ký biên bản xác nhận số liệu giao dịch thu hộ, phí thu hộ tháng 05/2025 với các thông tin sau:', red_text_format)
        
        # Section 1: Transaction fees
        worksheet.write('A10', '1. Số liệu giao dịch thu hộ', section_header_format)
        
        # Section 1 table
        worksheet.merge_range('A11:A12', 'Nhóm ngành', header_format)
        worksheet.merge_range('B11:B12', 'Số lượng', header_format)
        worksheet.merge_range('C11:C12', 'Tổng tiền (VNĐ)', header_format)
        
        worksheet.write('A13', '1/ Giao dịch phát sinh trong kỳ đối soát', cell_format)
        worksheet.write('B13', '', cell_center_format)
        worksheet.write('C13', '', cell_right_format)
        
        worksheet.write('A14', '2/ Giao dịch sai lệch của các kỳ trước đã được xử lý và thanh quyết toán bổ sung vào kỳ này', cell_format)
        worksheet.write('B14', '', cell_center_format)
        worksheet.write('C14', '', cell_right_format)
        
        worksheet.write('A15', 'Tổng cộng số tiền thu hộ SeABank thanh toán cho Dayone', cell_format)
        worksheet.write('B15', '', cell_center_format)
        worksheet.write('C15', '-', cell_right_format)
        
        worksheet.write('A16', 'Tổng thành tiền bằng chữ:', cell_format)
        worksheet.merge_range('B16:C16', '#NAME?', cell_format)
        
        # Section 2: Fee details
        worksheet.write('A18', '2. Số liệu phí thu hộ từ ngày 01/05/2025 đến ngày 31/05/2025', red_section_format)
        
        # Section 2 table headers
        worksheet.merge_range('A19:A20', 'Nhóm ngành', header_format)
        worksheet.merge_range('B19:B20', 'Giá trị Voucher phát sinh', header_format)
        worksheet.merge_range('C19:C20', 'Tỷ lệ phí áp dụng', header_format)
        worksheet.merge_range('D19:D20', 'Số tiền phí thu hộ (VNĐ)', header_format)
        
        # Section 2 data rows
        rows_data = [
            '1/ Giao dịch phát sinh trong kỳ đối soát',
            'a/ Nhà hàng, Cà phê &bánh, thời trang & làm đẹp',
            'b/ Mua sắm- Tiện ích',
            '2/ Giao dịch sai lệch của các kỳ trước đã được xử',
            'lý và thanh quyết toán bổ sung vào kỳ này',
            'a/ Nhà hàng, Cà phê &bánh, thời trang & làm đẹp',
            'b/ Mua sắm- Tiện ích',
            'Tổng cộng tiền chưa bao gồm VAT',
            'Số tiền VAT',
            'Tổng tiền phí thu hộ (bao gồm VAT) Dayone phải',
            'thanh toán cho SeABank:',
            'Tổng thành tiền bằng chữ :'
        ]
        
        for i, data in enumerate(rows_data):
            row = 21 + i
            worksheet.write(f'A{row}', data, cell_format)
            worksheet.write(f'B{row}', '-', cell_center_format)
            worksheet.write(f'C{row}', '', cell_center_format)
            worksheet.write(f'D{row}', '-', cell_right_format)
        
        # Section 3
        worksheet.write('A34', '3. Số liệu giao dịch thanh toán sai lệch trong kỳ đang chờ Hai bên xác nhận xử lý từ ngày 01/05/2025 đến ngày 31/05/2025:', red_section_format)
        
        # Section 3 table
        worksheet.merge_range('A35:A36', 'Nhóm ngành', header_format)
        worksheet.merge_range('B35:B36', 'Số lượng', header_format)
        worksheet.merge_range('C35:C36', 'Tổng tiền (VNĐ)', header_format)
        
        worksheet.write('A37', 'Got It Đà Nẵng', cell_format)
        worksheet.write('B37', '', cell_center_format)
        worksheet.write('C37', '', cell_right_format)
        
        worksheet.write('A38', 'Mua sắm', cell_format)
        worksheet.write('B38', '', cell_center_format)
        worksheet.write('C38', '', cell_right_format)
        
        worksheet.write('A39', 'Tổng', cell_format)
        worksheet.write('B39', '0', cell_center_format)
        worksheet.write('C39', '-', cell_right_format)
        
        worksheet.write('A40', 'Tổng thành tiền bằng chữ:', cell_format)
        
        # Section 4
        worksheet.write('A42', '4. Số liệu phí thu hộ sai lệch trong kỳ đang chờ xử lý', section_header_format)
        
        # Section 4 table
        worksheet.merge_range('A43:A44', 'Nhóm ngành', header_format)
        worksheet.merge_range('B43:B44', 'Giá trị Voucher phát sinh', header_format)
        worksheet.merge_range('C43:C44', 'Tỷ lệ phí áp dụng', header_format)
        worksheet.merge_range('D43:D44', 'Số tiền phí thu hộ (VNĐ)', header_format)
        
        rows_4_data = [
            'Got It Đà Nẵng',
            'Mua sắm',
            'Tổng cộng tiền chưa bao gồm VAT',
            'Số tiền VAT',
            'Tổng tiền phí (bao gồm VAT):',
            'Tổng thành tiền bằng chữ:'
        ]
        
        for i, data in enumerate(rows_4_data):
            row = 45 + i
            worksheet.write(f'A{row}', data, cell_format)
            worksheet.write(f'B{row}', '-', cell_center_format)
            worksheet.write(f'C{row}', '', cell_center_format)
            worksheet.write(f'D{row}', '-', cell_right_format)
        
        # Section 5
        worksheet.write('A52', '5. Số liệu sai lệch lũy kế đang chờ xử lý:', section_header_format)
        
        # Section 5 complex table
        worksheet.merge_range('A54:A56', 'Nhóm ngành', header_format)
        worksheet.merge_range('B54:C54', 'Tồn đầu kỳ', header_format)
        worksheet.merge_range('D54:F54', 'Phát sinh trong kỳ(*)', header_format)
        worksheet.merge_range('G54:H54', 'Đã xử lý trong kỳ', header_format)
        worksheet.merge_range('I54:J54', 'Tồn cuối kỳ', header_format)
        
        # Sub-headers for section 5
        worksheet.write('B55', 'Số lượng', header_format)
        worksheet.write('C55', 'Tổng tiền (VNĐ)', header_format)
        worksheet.write('D55', 'Số lượng', header_format)
        worksheet.write('E55', 'Tổng tiền (VNĐ)', header_format)
        worksheet.write('F55', 'Số lượng', header_format)
        worksheet.write('G55', 'Tổng tiền (VNĐ)', header_format)
        worksheet.write('H55', 'Số lượng', header_format)
        worksheet.write('I55', 'Tổng tiền (VNĐ)', header_format)
        worksheet.write('J55', '', header_format)
        
        worksheet.write('A57', 'Got It Đà Nẵng', cell_format)
        worksheet.write('A58', 'Mua sắm', cell_format)
        worksheet.write('A59', 'Tổng', cell_format)
        
        for row in [57, 58, 59]:
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                if row == 59 and col in ['B', 'C']:
                    worksheet.write(f'{col}{row}', '-', cell_center_format)
                else:
                    worksheet.write(f'{col}{row}', '-', cell_center_format)
        
        # Notes
        worksheet.write('A61', '(*)Phát sinh trong kỳ = bằng với số liệu bảng 3', cell_format)
        worksheet.write('A62', '(**) Đã xử lý trong kỳ (**) = bằng số liệu của chi tiết số 2 trong Bảng 1', cell_format)
        worksheet.write('A63', 'Biên bản này được lập thành 04 bản có giá trị pháp lý như nhau, mỗi bên giữ 02 bản.', cell_format)
        
        # Signature section
        worksheet.merge_range('A66:D66', 'ĐẠI DIỆN SEABANK', signature_format)
        worksheet.merge_range('F66:H66', 'ĐẠI DIỆN DAYONE', signature_format)
        
        worksheet.merge_range('A67:B67', 'Người lập', signature_format)
        worksheet.merge_range('C67:D67', 'Kiểm soát', signature_format)
        worksheet.merge_range('F67:H67', 'Đối soát', signature_format)
        
        worksheet.merge_range('A71:D71', 'Ban lãnh đạo', signature_format)
        worksheet.merge_range('F71:H71', 'Ban lãnh đạo', signature_format)

    def _create_chuyen_sang_thang_sau_sheet(self, workbook, worksheet, receipt):
        """Create chuyen sang thang sau sheet based on the fourth image"""
        # Define formats
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 8
        })
        
        # Set column widths to match the image exactly
        worksheet.set_column('A:A', 4)   # No
        worksheet.set_column('B:B', 15)  # Transaction_refid
        worksheet.set_column('C:C', 10)  # Issue_date
        worksheet.set_column('D:D', 15)  # Campaign_name
        worksheet.set_column('E:E', 15)  # Client_name
        worksheet.set_column('F:F', 12)  # Account_name
        worksheet.set_column('G:G', 12)  # Customer_name
        worksheet.set_column('H:H', 12)  # Customer_phone
        worksheet.set_column('I:I', 12)  # Product_name
        worksheet.set_column('J:J', 12)  # Merchant_code
        worksheet.set_column('K:K', 8)   # Price
        worksheet.set_column('L:L', 10)  # Expired_date
        worksheet.set_column('M:M', 8)   # Status
        worksheet.set_column('N:N', 12)  # category_brand
        
        # Headers - exactly as shown in the image
        headers = [
            'No', 'Transaction_refid', 'Issue_date', 'Campaign_name', 'Client_name', 
            'Account_name', 'Customer_name', 'Customer_phone', 'Product_name', 
            'Merchant_code', 'Price', 'Expired_date', 'Status', 'category_brand'
        ]
        
        # Write headers
        for i, header in enumerate(headers):
            worksheet.write(0, i, header, header_format)
        
        # Create one empty row as shown in the image
        for col in range(len(headers)):
            worksheet.write(1, col, '', cell_format)