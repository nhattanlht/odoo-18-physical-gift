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


class ReceiptTemplate3Exporter(models.AbstractModel):
    _name = 'receipt.template3.exporter'
    _description = 'Receipt Template 3 Excel Exporter'

    def export_template_3(self, receipt):
        """Export Excel receipt theo mẫu 3"""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("PT_in")
        worksheet_sms = workbook.add_worksheet("SMS")
        worksheet_phi_sms_dv = workbook.add_worksheet("Phí SMS+DV")
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
        page_number_format = workbook.add_format({
            'font_size': 24, 'color': '#808080', 'align': 'center', 'valign': 'vcenter'
        })

        # Set column widths
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 15)

        # Add vertical dotted lines to create the appearance of pages
        # These are visual separators as seen in the image
        worksheet.set_column('C:C', 12, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('F:F', 15, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('I:I', 12, None, {'hidden': False, 'level': 0, 'collapsed': False})

        # Company header (left) and Receipt title (right)
        worksheet.merge_range('A1:C1', 'CÔNG TY CỔ PHẦN DAYONE', company_header_format)
        worksheet.merge_range('D1:F1', 'PHIẾU THU', receipt_title_format)
        
        worksheet.merge_range(
            'A2:C2',
            'Tòa nhà 9-11 Nguyễn Văn Thủ, P. Đa Kao, Q.1',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.merge_range('A3:C3', 'Thành phố Hồ Chí Minh, Việt nam',
            workbook.add_format({'font_size': 12, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.merge_range('D3:F3', '00/00/2025', date_format)
        
        worksheet.merge_range('A4:C4', 'Mã số thuế/Tax Code : 0313249098',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        worksheet.merge_range('D4:F4', '00000000/DO/2025', 
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )
        
        # Bank account info
        worksheet.merge_range('A5:F5', 'Tài khoản ngân hàng số : 191.3341.5336.013, TECHCOMBANK, CN SÀI GÒN',
            workbook.add_format({'font_size': 11, 'valign': 'top', 'font_name': 'Calibri'})
        )

        # Payer section
        worksheet.merge_range('A7:F7', 'Người thanh toán', payer_header_format)
        
        worksheet.merge_range('A8:F8', 'CÔNG TY CỔ PHẦN MIOTO ASIA', table_cell_format)
        worksheet.merge_range('A9:F9', 'Số 2 Hồng Hà, Phường 2, Quận Tân Bình, TPHCM', table_cell_format)
        worksheet.merge_range('A10:F10', 'Mã số thuế : 0317307544', table_cell_format)

        # Table header
        worksheet.write('A12', 'CHI TIÊU', table_header_format)
        worksheet.write('B12', 'THÁNG 6/2025', table_header_format)
        worksheet.write('C12', 'SỐ LƯỢNG', table_header_format)
        worksheet.write('D12', 'ĐƠN GIÁ', table_header_format)
        worksheet.write('E12', 'VAT', table_header_format)
        worksheet.write('F12', 'THÀNH TIỀN', table_header_format)

        # Data rows
        row = 13
        worksheet.write(f'A{row}', '1', table_cell_format)
        worksheet.write(f'B{row}', 'Voucher Got It', table_cell_format)
        worksheet.write(f'C{row}', '', table_cell_format)
        worksheet.write(f'D{row}', '', table_cell_format)
        worksheet.write(f'E{row}', '', table_cell_format)
        worksheet.write(f'F{row}', '', table_number_format)

        # Total rows
        worksheet.merge_range(f'A{row+2}:E{row+2}', 'Tổng số tiền thanh toán', table_cell_format)
        worksheet.write(f'F{row+2}', '-', total_format)

        worksheet.merge_range(f'A{row+3}:E{row+3}', '', table_cell_format)
        worksheet.write(f'F{row+3}', '-', table_cell_format)

        worksheet.merge_range(f'A{row+4}:E{row+4}', '', table_cell_format)
        worksheet.write(f'F{row+4}', '-', table_cell_format)

        worksheet.merge_range(f'A{row+5}:E{row+5}', 'Tổng cộng', table_cell_format)
        worksheet.write(f'F{row+5}', '-', total_format)

        # Amount in words
        worksheet.write(f'A{row+7}', 'Bằng chữ :', table_cell_format)
        worksheet.merge_range(f'B{row+7}:F{row+7}', '', table_cell_format)

        # Signature section
        sig_row = row + 15
        worksheet.merge_range(f'D{sig_row}:F{sig_row}', 'Tên :', signature_format)
        worksheet.merge_range(f'D{sig_row+1}:F{sig_row+1}', 'Chức vụ :', signature_format)
        worksheet.merge_range(f'D{sig_row+2}:F{sig_row+2}', 'Ký và đóng dấu:', signature_format)

        # Footer
        footer_row = sig_row + 10
        worksheet.merge_range(f'A{footer_row}:F{footer_row}', 'Thank You For Doing Business With GOT IT !', footer_format)

        # Add page number indicators as seen in the image
        # Page 1 and Page 2
        worksheet.merge_range('A35:C35', 'Page 1', page_number_format)
        worksheet.merge_range('A70:C70', 'Page 2', page_number_format)
        
        # Page 3 and Page 4
        worksheet.merge_range('D35:F35', 'Page 3', page_number_format)
        worksheet.merge_range('D70:F70', 'Page 4', page_number_format)
        
        # Page 5 and Page 6 (in the far right column)
        worksheet.write('I35', 'Page 5', page_number_format)
        worksheet.write('I70', 'Page 6', page_number_format)
        
        # Create SMS sheet
        self._create_sms_sheet(workbook, worksheet_sms, receipt)
        
        # Create Phí SMS+DV sheet
        self._create_phi_sms_dv_sheet(workbook, worksheet_phi_sms_dv, receipt)
        
        # Create BK PHÍ DV sheet
        self._create_bk_phi_dv_sheet(workbook, worksheet_bk_phi_dv, receipt)
        
        # Create BANG KE-in sheet
        self._create_bang_ke_sheet(workbook, worksheet_bang_ke, receipt)

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = f"Phieu_Thu_Mau_3_{receipt.name.replace('/', '_') if receipt.name else 'new'}.xlsx"

        return file_content, filename
        
    def _create_bang_ke_sheet(self, workbook, worksheet, receipt):
        """Create BANG KE-in sheet based on the image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10, 'text_wrap': True
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9
        })
        
        # Set column widths
        worksheet.set_column('A:A', 4)   # Nc
        worksheet.set_column('B:B', 12)  # Issue_date
        worksheet.set_column('C:C', 15)  # Campaign_name
        worksheet.set_column('D:D', 15)  # Company_name
        worksheet.set_column('E:E', 15)  # Account_name
        worksheet.set_column('F:F', 10)  # Customer_id
        worksheet.set_column('G:G', 10)  # Customer_ph
        worksheet.set_column('H:H', 10)  # Customer_em
        worksheet.set_column('I:I', 12)  # Product_nam
        worksheet.set_column('J:J', 12)  # Merchant_co
        worksheet.set_column('K:K', 10)  # Price
        worksheet.set_column('L:L', 10)  # Expired_d
        worksheet.set_column('M:M', 12)  # Ref_id
        
        # Title
        worksheet.merge_range('A1:M1', 'BẢNG KÊ CHI TIẾT VOUCHER GOT IT', title_format)
        
        # Add vertical dotted lines to create the appearance of pages
        worksheet.set_column('C:C', 15, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('F:F', 10, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('I:I', 12, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('L:L', 10, None, {'hidden': False, 'level': 0, 'collapsed': False})
        
        # Headers
        worksheet.write('A2', 'Nc', header_format)
        worksheet.write('B2', 'Issue_date', header_format)
        worksheet.write('C2', 'Campaign_name', header_format)
        worksheet.write('D2', 'Company_name', header_format)
        worksheet.write('E2', 'Account_name', header_format)
        worksheet.write('F2', 'Customer_id', header_format)
        worksheet.write('G2', 'Customer_ph', header_format)
        worksheet.write('H2', 'Customer_em', header_format)
        worksheet.write('I2', 'Product_nam', header_format)
        worksheet.write('J2', 'Merchant_co', header_format)
        worksheet.write('K2', 'Price', header_format)
        worksheet.write('L2', 'Expired_d', header_format)
        worksheet.write('M2', 'Ref_id', header_format)
        
        # Create empty rows
        for i in range(1, 46):  # 45 rows as shown in the image
            row = i + 2  # Start from row 3
            worksheet.write(f'A{row}', i, cell_format)
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
                worksheet.write(f'{col}{row}', '', cell_format)
        
    def _create_phi_sms_dv_sheet(self, workbook, worksheet, receipt):
        """Create Phí SMS+DV sheet based on the image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10
        })
        
        # Set column widths
        worksheet.set_column('A:A', 6)   # STT
        worksheet.set_column('B:B', 15)  # Mã Đơn Hàng
        worksheet.set_column('C:C', 15)  # Tên sản phẩm
        worksheet.set_column('D:D', 12)  # Đơn vị tính
        worksheet.set_column('E:E', 12)  # Số lượng
        worksheet.set_column('F:F', 12)  # Đơn giá
        worksheet.set_column('G:G', 12)  # Thành tiền
        worksheet.set_column('H:H', 12)  # Thuế suất
        worksheet.set_column('I:I', 12)  # Tiền thuế
        worksheet.set_column('J:J', 15)  # Tổng tiền
        
        # Title
        worksheet.merge_range('A1:J1', 'HÓA ĐƠN GIÁ TRỊ GIA TĂNG', title_format)
        worksheet.merge_range('A2:J2', '(VAT INVOICE)', title_format)
        
        # Add invoice details
        worksheet.merge_range('A3:C3', 'Ngày (day)    tháng (month)    năm (year) 2024', cell_format)
        
        # Tax code section
        worksheet.merge_range('A5:J5', 'Mã của Cơ quan thuế:', cell_format)
        
        # Seller information
        worksheet.merge_range('A6:C6', 'Đơn vị bán hàng:', cell_format)
        worksheet.merge_range('D6:J6', 'CÔNG TY CỔ PHẦN DAYONE', cell_format)
        
        worksheet.merge_range('A7:C7', 'Mã số thuế (Tax code):', cell_format)
        worksheet.merge_range('D7:J7', '0 3 1 3 2 4 9 0 9 8', cell_format)
        
        worksheet.merge_range('A8:C8', 'Địa chỉ (Address):', cell_format)
        worksheet.merge_range('D8:J8', 'Tòa nhà 9-11 Nguyễn Văn Thủ, Phường Đa Kao, Quận 1, Thành phố Hồ Chí Minh, Việt Nam', cell_format)
        
        worksheet.merge_range('A9:C9', 'Điện thoại (Tel):', cell_format)
        worksheet.merge_range('D9:J9', '1900 55 88 20', cell_format)
        
        worksheet.merge_range('A10:C10', 'Số tài khoản (Acc No):', cell_format)
        worksheet.merge_range('D10:J10', '', cell_format)
        
        # Buyer information
        worksheet.merge_range('A11:C11', 'Họ tên người mua hàng (Buyer):', cell_format)
        worksheet.merge_range('D11:J11', '', cell_format)
        
        worksheet.merge_range('A12:C12', 'Tên đơn vị (Company):', cell_format)
        worksheet.merge_range('D12:J12', 'CÔNG TY CỔ PHẦN MIOTO ASIA', cell_format)
        
        worksheet.merge_range('A13:C13', 'Mã số thuế (Tax code):', cell_format)
        worksheet.merge_range('D13:J13', '0317307544', cell_format)
        
        worksheet.merge_range('A14:C14', 'Địa chỉ (Address):', cell_format)
        worksheet.merge_range('D14:J14', 'VP02, Tầng 08, Tòa nhà Pearl Plaza, Số 561A Điện Biên Phủ, Phường 25, Quận Bình Thạnh, Thành phố', cell_format)
        
        worksheet.merge_range('A15:C15', '', cell_format)
        worksheet.merge_range('D15:J15', 'Hồ Chí Minh, Việt Nam', cell_format)
        
        worksheet.merge_range('A16:C16', 'Số tài khoản (A/C No):', cell_format)
        worksheet.merge_range('D16:J16', '', cell_format)
        
        worksheet.merge_range('A17:C17', 'Hình thức thanh toán (Payment method):', cell_format)
        worksheet.merge_range('D17:J17', 'Tiền mặt/Chuyển khoản', cell_format)
        
        worksheet.merge_range('A18:C18', 'Thời hạn thanh toán (Payment term):', cell_format)
        worksheet.merge_range('D18:F18', '', cell_format)
        
        worksheet.merge_range('G18:H18', 'Ngày thanh toán (Due date):', cell_format)
        worksheet.merge_range('I18:J18', '', cell_format)
        
        # Table headers
        worksheet.write('A19', 'STT (No.)', header_format)
        worksheet.merge_range('B19:C19', 'Tên hàng hóa, dịch vụ (Description)', header_format)
        worksheet.write('D19', 'Đơn vị tính (Unit)', header_format)
        worksheet.write('E19', 'Số lượng (Quantity)', header_format)
        worksheet.write('F19', 'Đơn giá (Unit Price)', header_format)
        worksheet.merge_range('G19:H19', 'Thành tiền chưa có thuế GTGT (Amount excluding VAT)', header_format)
        worksheet.write('I19', 'Thuế suất (VAT rate)', header_format)
        worksheet.write('J19', 'Tiền thuế GTGT (Amount VAT)', header_format)
        
        # Data rows
        worksheet.write('A20', '1', cell_format)
        worksheet.merge_range('B20:C20', 'Phí dịch vụ tin nhắn đối với nhà mạng Mobifone/Vinaphone/Viettel', cell_format)
        worksheet.write('D20', 'Tin nhắn', cell_format)
        worksheet.write('E20', '', cell_format)
        worksheet.write('F20', '', cell_format)
        worksheet.merge_range('G20:H20', '', cell_format)
        worksheet.write('I20', '8%', cell_format)
        worksheet.write('J20', '', cell_format)
        
        worksheet.write('A21', '2', cell_format)
        worksheet.merge_range('B21:C21', 'Phí dịch vụ tin nhắn đối với nhà mạng Vietnammobile', cell_format)
        worksheet.write('D21', 'Tin nhắn', cell_format)
        worksheet.write('E21', '', cell_format)
        worksheet.write('F21', '', cell_format)
        worksheet.merge_range('G21:H21', '', cell_format)
        worksheet.write('I21', '8%', cell_format)
        worksheet.write('J21', '-', cell_format)
        
        worksheet.write('A22', '3', cell_format)
        worksheet.merge_range('B22:C22', 'Phí dịch vụ phát hành Voucher Got It đặc biệt', cell_format)
        worksheet.write('D22', 'Gói', cell_format)
        worksheet.write('E22', '', cell_format)
        worksheet.write('F22', '', cell_format)
        worksheet.merge_range('G22:H22', '', cell_format)
        worksheet.write('I22', '8%', cell_format)
        worksheet.write('J22', '-', cell_format)
        
        # Month row
        worksheet.merge_range('A23:B23', 'Tháng 06/2025', cell_format)
        worksheet.merge_range('C23:J23', '', cell_format)
        
        # Summary rows
        worksheet.merge_range('A24:F24', 'Cộng tiền hàng chưa có thuế GTGT (Total amount excluding VAT):', cell_format)
        worksheet.merge_range('G24:J24', '-', cell_format)
        
        # Summary table
        worksheet.merge_range('A26:C26', 'Tổng hợp (In Summary)', header_format)
        worksheet.merge_range('D26:E26', 'Thuế suất (VAT rate)', header_format)
        worksheet.merge_range('F26:G26', 'Trị giá chưa thuế GTGT (Amount excluding VAT)', header_format)
        worksheet.write('H26', 'Tiền thuế GTGT (Amount VAT)', header_format)
        worksheet.merge_range('I26:J26', 'Trị giá thanh toán (Amount including VAT)', header_format)
        
        # Summary data rows
        worksheet.merge_range('A27:C27', 'Hàng hóa không phải kê khai và tính thuế GTGT', cell_format)
        worksheet.merge_range('D27:E27', '', cell_format)
        worksheet.merge_range('F27:G27', '0', cell_format)
        worksheet.write('H27', '\\', cell_format)
        worksheet.merge_range('I27:J27', '0', cell_format)
        
        worksheet.merge_range('A28:C28', 'Hàng hóa không chịu thuế GTGT', cell_format)
        worksheet.merge_range('D28:E28', '', cell_format)
        worksheet.merge_range('F28:G28', '0', cell_format)
        worksheet.write('H28', '\\', cell_format)
        worksheet.merge_range('I28:J28', '0', cell_format)
        
        worksheet.merge_range('A29:C29', 'Hàng hóa chịu thuế suất:', cell_format)
        worksheet.merge_range('D29:E29', '0%', cell_format)
        worksheet.merge_range('F29:G29', '0', cell_format)
        worksheet.write('H29', '0', cell_format)
        worksheet.merge_range('I29:J29', '0', cell_format)
        
        worksheet.merge_range('A30:C30', 'Hàng hóa chịu thuế suất:', cell_format)
        worksheet.merge_range('D30:E30', '5%', cell_format)
        worksheet.merge_range('F30:G30', '0', cell_format)
        worksheet.write('H30', '0', cell_format)
        worksheet.merge_range('I30:J30', '0', cell_format)
        
        worksheet.merge_range('A31:C31', 'Hàng hóa chịu thuế suất:', cell_format)
        worksheet.merge_range('D31:E31', '8%', cell_format)
        worksheet.merge_range('F31:G31', '-', cell_format)
        worksheet.write('H31', '-', cell_format)
        worksheet.merge_range('I31:J31', '-', cell_format)
        
        worksheet.merge_range('A32:C32', 'Hàng hóa chịu thuế suất:', cell_format)
        worksheet.merge_range('D32:E32', '10%', cell_format)
        worksheet.merge_range('F32:G32', '0', cell_format)
        worksheet.write('H32', '0', cell_format)
        worksheet.merge_range('I32:J32', '0', cell_format)
        
        # Total row
        worksheet.merge_range('A33:C33', 'Tổng cộng tiền thanh toán (Total):', cell_format)
        worksheet.merge_range('D33:E33', '', cell_format)
        worksheet.merge_range('F33:G33', '-', cell_format)
        worksheet.write('H33', '-', cell_format)
        worksheet.merge_range('I33:J33', '-', cell_format)
        
        # Amount in words
        worksheet.merge_range('A34:J34', 'Tổng số tiền viết bằng chữ (Amount in words):', cell_format)
        
        # Signatures
        worksheet.merge_range('A36:E36', 'Người mua hàng (Buyer)', header_format)
        worksheet.merge_range('F36:J36', 'Người bán hàng (Seller)', header_format)
        
    def _create_bk_phi_dv_sheet(self, workbook, worksheet, receipt):
        """Create BK PHÍ DV sheet based on the image"""
        # Define formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10, 'text_wrap': True
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9
        })
        
        # Set column widths
        worksheet.set_column('A:A', 4)   # No
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
        
        # Headers
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
        
        # Add vertical dotted lines to create the appearance of pages
        worksheet.set_column('C:C', 20, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('F:F', 12, None, {'hidden': False, 'level': 0, 'collapsed': False})
        worksheet.set_column('I:I', 18, None, {'hidden': False, 'level': 0, 'collapsed': False})
        
        # Page numbers
        worksheet.merge_range('A12:C12', 'Page 1', workbook.add_format({
            'font_size': 24, 'color': '#808080', 'align': 'center', 'valign': 'vcenter'
        }))
        worksheet.merge_range('D12:F12', 'Page 11', workbook.add_format({
            'font_size': 24, 'color': '#808080', 'align': 'center', 'valign': 'vcenter'
        }))
        worksheet.merge_range('G12:J12', 'Page 21', workbook.add_format({
            'font_size': 24, 'color': '#808080', 'align': 'center', 'valign': 'vcenter'
        }))
        
        # Sample data rows
        for i in range(1, 26):  # Create 25 rows
            row = i + 6  # Start from row 7
            if i <= 2:  # Only add data for first two rows as shown in the image
                worksheet.write(f'A{row}', f'[NO]', cell_format)
                worksheet.write(f'B{row}', '[VOUCHER_ISSUED_TIME]', cell_format)
                worksheet.write(f'C{row}', '[ORDER_NAME]', cell_format)
                worksheet.write(f'D{row}', '[COMPANY_NAME]', cell_format)
                worksheet.write(f'E{row}', '[ACCOUNT_NAME]', cell_format)
                worksheet.write(f'F{row}', '[VOUCHER_VALUE]', cell_format)
                worksheet.write(f'G{row}', '[VOUCHER_TRANSACTION_REFID]', cell_format)
                worksheet.write(f'H{row}', '[PRODUCT_NAME]', cell_format)
                worksheet.write(f'I{row}', '[PRODUCT_BRAND]', cell_format)
                worksheet.write(f'J{row}', '', cell_format)
            else:
                # Empty cells for remaining rows
                for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                    worksheet.write(f'{col}{row}', '', cell_format)
        
        # Total rows
        total_row = 32
        worksheet.merge_range(f'A{total_row}:E{total_row}', 'TỔNG', header_format)
        worksheet.write(f'F{total_row}', '-', cell_format)
        
        worksheet.merge_range(f'A{total_row+1}:E{total_row+1}', '% PHÍ DỊCH VỤ', header_format)
        worksheet.write(f'F{total_row+1}', '-', cell_format)
        
        worksheet.merge_range(f'A{total_row+2}:E{total_row+2}', 'PHÍ DỊCH VỤ', header_format)
        worksheet.write(f'F{total_row+2}', '-', cell_format)
        
    def _create_sms_sheet(self, workbook, worksheet, receipt):
        """Create SMS sheet based on the image"""
        # Define formats
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10
        })
        number_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'font_size': 10, 'num_format': '#,##0'
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'right', 'valign': 'vcenter',
            'font_size': 10, 'num_format': '#,##0'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 15)  # SEND TIME
        worksheet.set_column('B:B', 15)  # MOBILE NUMBER
        worksheet.set_column('C:C', 15)  # BRANDNAME
        worksheet.set_column('D:D', 10)  # STATUS
        worksheet.set_column('E:E', 8)   # OPERA
        worksheet.set_column('F:F', 8)   # M
        worksheet.set_column('G:G', 8)   # T
        worksheet.set_column('H:H', 15)  # ORDER NAME
        worksheet.set_column('I:I', 15)  # COMPANY NAME
        worksheet.set_column('J:J', 15)  # ACCOUNT NAME
        worksheet.set_column('K:K', 15)  # Empty
        
        # Headers row
        worksheet.write('A1', 'SEND TIME', header_format)
        worksheet.write('B1', 'MOBILE NUMBER', header_format)
        worksheet.write('C1', 'BRANDNAME', header_format)
        worksheet.write('D1', 'STATUS', header_format)
        worksheet.write('E1', 'OPERA', header_format)
        worksheet.write('F1', 'M', header_format)
        worksheet.write('G1', 'T', header_format)
        worksheet.write('H1', 'ORDER NAME', header_format)
        worksheet.write('I1', 'COMPANY NAME', header_format)
        worksheet.write('J1', 'ACCOUNT NAME', header_format)
        worksheet.write('K1', 'Row Labels', header_format)
        worksheet.write('L1', 'Sum of MT', header_format)
        
        # Data rows - based on the image
        worksheet.write('K2', 'Mobifone', cell_format)
        worksheet.write('L2', 165, number_format)
        
        worksheet.write('K3', 'Vietnamobile', cell_format)
        worksheet.write('L3', 17, number_format)
        
        worksheet.write('K4', 'Viettel', cell_format)
        worksheet.write('L4', 156, number_format)
        
        worksheet.write('K5', 'Vinaphone', cell_format)
        worksheet.write('L5', 73, number_format)
        
        worksheet.write('K6', '(blank)', cell_format)
        worksheet.write('L6', '', cell_format)
        
        # Total row
        worksheet.write('K7', 'Grand Total', total_format)
        worksheet.write('L7', 411, total_format)