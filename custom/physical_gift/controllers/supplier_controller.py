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
            
            # Tạo domain filter
            domain = [('active', '=', True)]
            
            # Tìm kiếm theo tên
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs.get('name')))
            
            # Lấy dữ liệu
            suppliers = request.env['physical.gift.supplier'].sudo().search(
                domain, 
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
                    'active': supplier.active,
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