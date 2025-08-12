# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class SupplierController(http.Controller):
    """API Controller cho Physical Gift Supplier"""
    
    @http.route('/api/physical-gift/suppliers', type='http', auth='public', methods=['GET'], csrf=False)
    def get_suppliers(self, **kwargs):
        """Lấy danh sách nhà cung cấp"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Lấy dữ liệu
            suppliers = request.env['physical.gift.supplier'].sudo().search(
                [],
                limit=limit, 
                offset=offset,
                order='name'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for supplier in suppliers:
                data.append({
                    'id': supplier.id,
                    'name': supplier.name,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(suppliers)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 

    @http.route('/api/physical-gift/suppliers', type='http', auth='public', methods=['POST'], csrf=False)
    def create_supplier(self, **kwargs):
        """Tạo nhà cung cấp"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required = ['name', 'full_name']
            for field in required:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name': data.get('name'),
                'full_name': data.get('full_name'),
                'representative_name': data.get('representative_name'),
                'tax_code': data.get('tax_code'),
                'account_number': data.get('account_number'),
                'bank_name': data.get('bank_name'),
                'warehouse_code': data.get('warehouse_code'),
                'state': data.get('state', 'active'),
                'logo': data.get('logo'),
            }
            supplier = request.env['physical.gift.supplier'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': supplier.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/suppliers/<int:supplier_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_supplier(self, supplier_id, **kwargs):
        """Cập nhật nhà cung cấp"""
        try:
            supplier = request.env['physical.gift.supplier'].sudo().browse(supplier_id)
            if not supplier.exists():
                return json.dumps({'success': False, 'error': 'Nhà cung cấp không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name', 'full_name', 'representative_name', 'tax_code', 'account_number', 'bank_name', 'warehouse_code', 'state', 'logo']
            vals = {k: data.get(k) for k in allowed if k in data}
            if vals:
                supplier.write(vals)
            return json.dumps({'success': True, 'data': {'id': supplier.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/suppliers/<int:supplier_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_supplier(self, supplier_id, **kwargs):
        """Xoá nhà cung cấp"""
        try:
            supplier = request.env['physical.gift.supplier'].sudo().browse(supplier_id)
            if not supplier.exists():
                return json.dumps({'success': False, 'error': 'Nhà cung cấp không tồn tại'}, ensure_ascii=False)
            supplier.unlink()
            return json.dumps({'success': True, 'data': {'id': supplier_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)