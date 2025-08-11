# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class CategoryController(http.Controller):
    """API Controller cho Physical Gift Category"""
    
    @http.route('/api/physical-gift/categories', type='http', auth='public', methods=['GET'], csrf=False)
    def get_categories(self, **kwargs):
        """Lấy danh sách danh mục"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Tạo domain filter
            domain = []
            
            # Tìm kiếm theo tên
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs.get('name')))
            
            # Tìm kiếm theo mã
            if kwargs.get('code'):
                domain.append(('code', 'ilike', kwargs.get('code')))
            
            # Filter theo parent_id
            if kwargs.get('parent_id'):
                domain.append(('parent_id', '=', int(kwargs.get('parent_id'))))
            
            # Lấy dữ liệu
            categories = request.env['physical.gift.category'].sudo().search(
                domain, 
                limit=limit, 
                offset=offset,
                order='sequence, name'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for category in categories:
                data.append({
                    'id': category.id,
                    'name': category.name,
                    'name_en': category.name_en,
                    'code': category.code,
                    'description': category.description,
                    'parent_id': category.parent_id.id if category.parent_id else None,
                    'parent_name': category.parent_id.name if category.parent_id else None,
                    'sequence': category.sequence,
                    'item_count': category.item_count,
                    'program_count': category.program_count,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(categories)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 