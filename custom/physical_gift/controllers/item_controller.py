# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class ItemController(http.Controller):
    """API Controller cho Physical Gift Item"""
    
    @http.route('/api/physical-gift/items', type='http', auth='public', methods=['GET'], csrf=False)
    def get_items(self, **kwargs):
        """Lấy danh sách sản phẩm"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Tạo domain filter
            domain = [('active', '=', True)]
            
            # Filter theo brand_id
            if kwargs.get('brand_id'):
                domain.append(('brand_id', '=', int(kwargs.get('brand_id'))))
            
            # Filter theo category_id
            if kwargs.get('category_id'):
                domain.append(('category_id', '=', int(kwargs.get('category_id'))))
            
            # Filter theo supplier_id
            if kwargs.get('supplier_id'):
                domain.append(('supplier_id', '=', int(kwargs.get('supplier_id'))))
            
            # Tìm kiếm theo tên
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs.get('name')))
            
            # Lấy dữ liệu
            items = request.env['physical.gift.item'].sudo().search(
                domain, 
                limit=limit, 
                offset=offset,
                order='name'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for item in items:
                data.append({
                    'id': item.id,
                    'name': item.name,
                    'brand_id': item.brand_id.id if item.brand_id else None,
                    'brand_name': item.brand_id.name if item.brand_id else None,
                    'category_id': item.category_id.id if item.category_id else None,
                    'category_name': item.category_id.name if item.category_id else None,
                    'supplier_id': item.supplier_id.id if item.supplier_id else None,
                    'supplier_name': item.supplier_id.name if item.supplier_id else None,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'total_price': item.total_price,
                    'active': item.active,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(items)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 