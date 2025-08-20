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


class ReceiptTemplate2Exporter(models.AbstractModel):
    _name = 'receipt.template2.exporter'
    _description = 'Receipt Template 2 Excel Exporter'

    def export_template_2(self, receipt):
        """Export Excel receipt theo mẫu 2"""
        if xlsxwriter is None:
            raise UserError(_("Module xlsxwriter is required to export Excel. Please install python-xlsxwriter."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Phiếu Thu")
        worksheet_phi_giao_hang = workbook.add_worksheet("Phi Giao Hang PS")
        worksheet_summary = workbook.add_worksheet("BẢNG KÊ SUMMARY")
        worksheet_loyalty = workbook.add_worksheet("BẢNG KÊ LOYALTY")

        # Define formats theo chính xác hình ảnh
        company_header_format = workbook.add_format({
            'bold': True, 'font_size': 18, 'valign': 'top', 'font_name': 'Times New Roman'
        })
        receipt_title_format = workbook.add_format({
            'bold': True, 'font_size': 20, 'align': 'right', 'valign': 'top', 'font_name': 'Arial'
        })
        info_format = workbook.add_format({
            'font_size': 11, 'valign': 'top', 'font_name': 'Arial'
        })
        date_format = workbook.add_format({
            'align': 'right', 'font_size': 11, 'valign': 'top', 'font_name': 'Arial'
        })
        payer_header_format = workbook.add_format({
            'bold': True, 'align': 'left', 'valign': 'vcenter', 'border': 1, 'font_size': 11, 'font_name': 'Arial'
        })
        table_header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'font_size': 10, 'font_name': 'Arial'
        })
        table_cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Arial'
        })
        table_number_format = workbook.add_format({
            'border': 1, 'align': 'right', 'valign': 'vcenter',
            'font_size': 10, 'font_name': 'Arial'
        })
        total_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'right', 'valign': 'vcenter',
            'font_size': 10, 'font_name': 'Arial'
        })
        signature_format = workbook.add_format({
            'align': 'center', 'valign': 'top', 'font_size': 10, 'bold': True, 'font_name': 'Arial'
        })

        # Set column widths theo hình ảnh
        worksheet.set_column('A:A', 4)   # STT
        worksheet.set_column('B:B', 35)  # HÀNG HÓA
        worksheet.set_column('C:C', 12)  # SỐ LƯỢNG  
        worksheet.set_column('D:D', 12)  # ĐƠN GIÁ
        worksheet.set_column('E:E', 15)  # THÀNH TIỀN

        # Header giống hình ảnh - Company bên trái, PHIẾU THU bên phải
        worksheet.write('A1', 'CÔNG TY CỔ PHẦN DAYONE', company_header_format)
        worksheet.merge_range('D1:E1', 'PHIẾU THU', receipt_title_format)
        
        worksheet.merge_range('A2:C2', 'Số 102 Nguyễn Đình Chiểu, Phường 15, Quận Phú Nhuận, TP.HCM, Việt Nam', info_format)
        worksheet.merge_range('D2:E2', f'Ngày: {receipt.receipt_date.strftime("%d/%m/%Y")}', date_format)
        
        worksheet.write('A3', f'Mã số thuế/ Tax Code : {receipt.company_id.vat or "0313249098"}', info_format)
        worksheet.merge_range('D3:E3', f'Ký hiệu: {receipt.name or "DO"}', date_format)
        worksheet.merge_range('D4:E4', f'Số: {"." * 18}', date_format)
        
        # Tài khoản ngân hàng
        worksheet.merge_range('A4:C4', 'Tài khoản ngân hàng số: 1081100323005, MB BANK - ĐINH TIẾN HOÀNG', info_format)

        # Người mua section
        worksheet.write('A6', 'Người mua', payer_header_format)
        worksheet.merge_range('A7:E7', receipt.payer_name or 'CÔNG TY TNHH BẢO HIỂM NHÂN THỌ SUN LIFE VIỆT NAM', table_cell_format)
        worksheet.merge_range('A8:E8', receipt.payer_address or 'Tầng L29, Tòa nhà Vietcombank Tower, số 5 công trường Mê Linh, Phường Bến Nghé, Q1, TP.HCM', table_cell_format)
        worksheet.merge_range('A9:E9', f'Mã số thuế/ Tax Code: {receipt.payer_tax_code or "0312149397"}', table_cell_format)

        # Table header với THÁNG 05.2025
        worksheet.write('A11', 'STT', table_header_format)
        worksheet.write('B11', 'HÀNG HÓA', table_header_format)  
        worksheet.write('C11', 'SỐ LƯỢNG', table_header_format)
        worksheet.write('D11', 'ĐƠN GIÁ', table_header_format)
        worksheet.write('E11', 'THÀNH TIỀN', table_header_format)
        
        # Sub-header với THÁNG
        worksheet.merge_range('A12:E12', f'THÁNG {receipt.receipt_date.strftime("%m.%Y")}', table_header_format)

        # Data rows - Chính xác 45 dòng như hình
        row_start = 13
        for i in range(1, 46):  # 45 dòng
            current_row = row_start + i - 1
            worksheet.write(f'A{current_row}', i, table_cell_format)
            
            if i <= 4:
                worksheet.write(f'B{current_row}', 'Voucher Got It', table_cell_format)
            else:
                worksheet.write(f'B{current_row}', 'Voucher Got It - Quà tặng Vật lý', table_cell_format)
            
            worksheet.write(f'C{current_row}', '', table_cell_format)  # Số lượng trống
            worksheet.write(f'D{current_row}', '', table_cell_format)  # Đơn giá trống
            worksheet.write(f'E{current_row}', 0, table_number_format)  # Thành tiền = 0

        # Total row
        total_row = row_start + 45
        worksheet.merge_range(f'A{total_row}:D{total_row}', 'Tổng cộng:', total_format)
        worksheet.write(f'E{total_row}', 0, total_format)

        # Bằng chữ section
        bang_chu_row = total_row + 2
        worksheet.write(f'A{bang_chu_row}', 'Bằng chữ:', table_cell_format)
        worksheet.merge_range(f'B{bang_chu_row}:E{bang_chu_row}', '', table_cell_format)

        # Footer signature - theo hình ảnh
        footer_row = bang_chu_row + 5
        worksheet.merge_range(f'C{footer_row}:E{footer_row}', 'ĐẠI DIỆN CÔNG TY CỔ PHẦN DAYONE', signature_format)
        worksheet.merge_range(f'C{footer_row+1}:E{footer_row+1}', 'KÝ VÀ ĐÓNG DẤU', signature_format)

        # === SHEET 2: Phi Giao Hang PS ===
        self._create_phi_giao_hang_ps_sheet(workbook, worksheet_phi_giao_hang, receipt)

        # === SHEET 3: BẢNG KÊ SUMMARY ===
        self._create_summary_sheet(workbook, worksheet_summary, receipt)

        # === SHEET 4: BẢNG KÊ LOYALTY ===
        self._create_loyalty_sheet(workbook, worksheet_loyalty, receipt)

        workbook.close()
        output.seek(0)

        file_content = base64.b64encode(output.read())
        filename = f"Phieu_Thu_Mau_2_{receipt.name.replace('/', '_')}.xlsx"

        return file_content, filename

    def _create_phi_giao_hang_ps_sheet(self, workbook, worksheet, receipt):
        """Tạo sheet Phi Giao Hang PS theo mẫu hình ảnh"""
        # Define formats cho sheet Phi Giao Hang PS
        title_format = workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Arial'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 10, 'text_wrap': True, 'font_name': 'Arial'
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9, 'font_name': 'Arial'
        })
        summary_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter',
            'font_size': 10, 'font_name': 'Arial'
        })
        dash_format = workbook.add_format({
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'font_size': 10, 'font_name': 'Arial'
        })

        # Set column widths theo hình ảnh
        worksheet.set_column('A:A', 6)   # STT
        worksheet.set_column('B:B', 15)  # Mã Đơn Hàng
        worksheet.set_column('C:C', 12)  # Ngày tạo đơn hàng
        worksheet.set_column('D:D', 8)   # Tháng
        worksheet.set_column('E:E', 12)  # Voucher Code
        worksheet.set_column('F:F', 12)  # Mã quà tặng KH xác nhận
        worksheet.set_column('G:G', 25)  # Loại quà tặng KH xác nhận
        worksheet.set_column('H:H', 12)  # Mã vận đơn
        worksheet.set_column('I:I', 12)  # Giao hàng thành công
        worksheet.set_column('J:J', 12)  # Giao lại lần 4
        worksheet.set_column('K:K', 8)   # Ghi chú
        worksheet.set_column('L:L', 20)  # Phí giao hàng Sunmart phát sinh

        # Title
        worksheet.merge_range('A1:L1', 'BẢNG KÊ PHÍ GIAO HÀNG PHÁT SINH', title_format)

        # Headers
        worksheet.write('A3', 'STT', header_format)
        worksheet.write('B3', 'Mã Đơn Hàng', header_format)
        worksheet.write('C3', 'Ngày tạo đơn hàng', header_format)
        worksheet.write('D3', 'Tháng', header_format)
        worksheet.write('E3', 'Voucher Code', header_format)
        worksheet.write('F3', 'Mã quà tặng KH xác nhận', header_format)
        worksheet.write('G3', 'Loại quà tặng KH xác nhận', header_format)
        worksheet.write('H3', 'Mã vận đơn', header_format)
        worksheet.write('I3', 'Giao hàng thành công', header_format)
        worksheet.write('J3', 'Giao lại lần 4', header_format)
        worksheet.write('K3', 'Ghi chú', header_format)
        worksheet.write('L3', 'Phí giao hàng Sunmart phát sinh', header_format)

        # Data row (1 dòng trống như trong hình)
        worksheet.write('A4', '1', cell_format)
        for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
            worksheet.write(f'{col}4', '', cell_format)

        # Summary rows
        worksheet.merge_range('A5:K5', 'Số tiền trước VAT', summary_format)
        worksheet.write('L5', '-', dash_format)
        
        worksheet.merge_range('A6:K6', 'VAT 8%', summary_format)
        worksheet.write('L6', '-', dash_format)
        
        worksheet.merge_range('A7:K7', 'TỔNG CỘNG', summary_format)
        worksheet.write('L7', '-', dash_format)

    def _create_summary_sheet(self, workbook, worksheet, receipt):
        """Tạo sheet BẢNG KÊ SUMMARY theo mẫu hình ảnh"""
        # Define formats cho sheet Summary
        title_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Arial'
        })
        # Format cho header màu vàng (cột H đến J)
        yellow_header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9, 'text_wrap': True, 'font_name': 'Arial',
            'bg_color': '#FFFF00'  # Yellow background như trong hình
        })
        # Format cho header màu xanh lá cây (các cột còn lại)
        green_header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9, 'text_wrap': True, 'font_name': 'Arial',
            'bg_color': '#92D050'  # Màu xanh lá cây như trong hình
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9, 'font_name': 'Arial'
        })
        dash_format = workbook.add_format({
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'font_size': 9, 'font_name': 'Arial'
        })

        # Set column widths theo hình ảnh
        worksheet.set_column('A:A', 6)   # STT
        worksheet.set_column('B:B', 12)  # Mã khách hàng
        worksheet.set_column('C:C', 8)   # Điểm
        worksheet.set_column('D:D', 12)  # Tổng đơn điểm
        worksheet.set_column('E:E', 12)  # Ngày thực hiện
        worksheet.set_column('F:F', 10)  # Loại quà tặng
        worksheet.set_column('G:G', 8)   # Số lượng
        worksheet.set_column('H:H', 12)  # Voucher Code
        worksheet.set_column('I:I', 8)   # Ref Id
        worksheet.set_column('J:J', 12)  # Giá trị quà tặng
        worksheet.set_column('K:K', 12)  # Trạng thái giao quà
        worksheet.set_column('L:L', 10)  # Chi phí vận chuyển
        worksheet.set_column('M:M', 12)  # Địa chỉ giao hàng
        worksheet.set_column('N:N', 10)  # Thành phố
        worksheet.set_column('O:O', 8)   # Mã bill
        worksheet.set_column('P:P', 8)   # SKU
        worksheet.set_column('Q:Q', 10)  # Tên hàng
        worksheet.set_column('R:R', 12)  # Phí vận hàng Sunmart
        worksheet.set_column('S:S', 10)  # Số tiền phải vận hành
        worksheet.set_column('T:T', 12)  # Phí giao hàng Sunmart
        worksheet.set_column('U:U', 10)  # Phí đóng gói

        # Title
        worksheet.merge_range('A1:U1', 'BẢNG KÊ ĐỐI SOÁT VÀ THANH TOÁN', title_format)

        # Headers - dòng 2
        worksheet.write('A2', 'STT', yellow_header_format)
        worksheet.write('B2', 'Mã khách hàng', yellow_header_format)
        worksheet.write('C2', 'Điểm quy đổi', yellow_header_format)
        worksheet.write('D2', 'Tổng dư điểm', yellow_header_format)
        worksheet.write('E2', 'Ngày thực hiện', yellow_header_format)
        worksheet.write('F2', 'Loại quà tặng', yellow_header_format)
        worksheet.write('G2', 'Số lượng', yellow_header_format)
        worksheet.write('H2', 'Voucher Code', yellow_header_format)
        worksheet.write('I2', 'Ref Id', yellow_header_format)
        worksheet.write('J2', 'Giá trị quà tặng', yellow_header_format)
        worksheet.write('K2', 'Trạng thái giao quà', yellow_header_format)
        worksheet.write('L2', 'Chi phí vận chuyển', yellow_header_format)
        worksheet.write('M2', 'Địa chỉ giao hàng', yellow_header_format)
        worksheet.write('N2', 'Thành phố', green_header_format)
        worksheet.write('O2', 'Mã bill', green_header_format)
        worksheet.write('P2', 'SKU', green_header_format)
        worksheet.write('Q2', 'Tên hàng', green_header_format)
        worksheet.write('R2', 'Phí vận hành Sunmart', green_header_format)
        worksheet.write('S2', 'Số tiền phí vận hành', green_header_format)
        worksheet.write('T2', 'Phí giao hàng Sunmart', green_header_format)
        worksheet.write('U2', 'Phí đóng gói', green_header_format)

        # Data rows - 33 dòng trống như trong hình
        for i in range(1, 34):  # 33 dòng từ 3-35
            row = i + 2
            worksheet.write(f'A{row}', i, cell_format)
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
                worksheet.write(f'{col}{row}', '', cell_format)  # Empty cells
            # Cột cuối cùng (U) có dấu '-'
            worksheet.write(f'U{row}', '-', cell_format)

    def _create_loyalty_sheet(self, workbook, worksheet, receipt):
        """Tạo sheet BẢNG KÊ LOYALTY theo mẫu hình ảnh"""
        # Define formats cho sheet Loyalty
        title_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'font_name': 'Arial'
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9, 'text_wrap': True, 'font_name': 'Arial',
            'bg_color': '#FFFF00'  # Yellow background như trong hình
        })
        
        # Format cho header màu xanh lá cây (cột O đến U)
        green_header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_size': 9, 'text_wrap': True, 'font_name': 'Arial',
            'bg_color': '#92D050'  # Màu xanh lá cây như trong hình
        })
        cell_format = workbook.add_format({
            'border': 1, 'valign': 'vcenter', 'font_size': 9, 'font_name': 'Arial'
        })

        # Set column widths theo hình ảnh
        worksheet.set_column('A:A', 6)   # STT
        worksheet.set_column('B:B', 12)  # Mã khách hàng
        worksheet.set_column('C:C', 8)   # Điểm quy đổi
        worksheet.set_column('D:D', 12)  # Tổng dư điểm
        worksheet.set_column('E:E', 12)  # Ngày thực hiện
        worksheet.set_column('F:F', 10)  # Loại quà tặng
        worksheet.set_column('G:G', 8)   # Số lượng
        worksheet.set_column('H:H', 12)  # Voucher Code
        worksheet.set_column('I:I', 8)   # Ref Id
        worksheet.set_column('J:J', 12)  # Giá trị quà tặng
        worksheet.set_column('K:K', 12)  # Trạng thái giao quà
        worksheet.set_column('L:L', 10)  # Chi phí vận chuyển
        worksheet.set_column('M:M', 12)  # Địa chỉ giao hàng
        worksheet.set_column('N:N', 10)  # Thành phố
        worksheet.set_column('O:O', 8)   # Mã bill
        worksheet.set_column('P:P', 8)   # SKU
        worksheet.set_column('Q:Q', 10)  # Tên hàng
        worksheet.set_column('R:R', 12)  # Phí vận hành Sunmart
        worksheet.set_column('S:S', 10)  # Số tiền phí vận hành
        worksheet.set_column('T:T', 12)  # Phí giao hàng Sunmart
        worksheet.set_column('U:U', 10)  # Phí đóng gói

        # Title
        worksheet.merge_range('A1:U1', 'BẢNG KÊ ĐỐI SOÁT VÀ THANH TOÁN', title_format)

        # Headers - dòng 2
        worksheet.write('A2', 'STT', header_format)
        worksheet.write('B2', 'Mã khách hàng', header_format)
        worksheet.write('C2', 'Điểm quy đổi', header_format)
        worksheet.write('D2', 'Tổng dư điểm', header_format)
        worksheet.write('E2', 'Ngày thực hiện', header_format)
        worksheet.write('F2', 'Loại quà tặng', header_format)
        worksheet.write('G2', 'Số lượng', header_format)
        worksheet.write('H2', 'Voucher Code', header_format)
        worksheet.write('I2', 'Ref Id', header_format)
        worksheet.write('J2', 'Giá trị quà tặng', header_format)
        worksheet.write('K2', 'Trạng thái giao quà', header_format)
        worksheet.write('L2', 'Chi phí vận chuyển', header_format)
        worksheet.write('M2', 'Địa chỉ giao hàng', header_format)
        worksheet.write('N2', 'Thành phố', header_format)
        worksheet.write('O2', 'Mã bill', green_header_format)
        worksheet.write('P2', 'SKU', green_header_format)
        worksheet.write('Q2', 'Tên hàng', green_header_format)
        worksheet.write('R2', 'Phí vận hành Sunmart', green_header_format)
        worksheet.write('S2', 'Số tiền phí vận hành', green_header_format)
        worksheet.write('T2', 'Phí giao hàng Sunmart', green_header_format)
        worksheet.write('U2', 'Phí đóng gói', green_header_format)

        # Data rows - 100 dòng như trong hình (từ 3-102)
        for i in range(1, 101):  # 100 dòng từ 3-102
            row = i + 2
            worksheet.write(f'A{row}', i, cell_format)
            for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
                worksheet.write(f'{col}{row}', '', cell_format)  # Empty cells
            # Cột cuối cùng (U) có dấu '-'
            worksheet.write(f'U{row}', '-', cell_format)