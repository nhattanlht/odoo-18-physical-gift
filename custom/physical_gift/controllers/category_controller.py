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

    @http.route('/api/physical-gift/categories', type='http', auth='public', methods=['POST'], csrf=False)
    def create_category(self, **kwargs):
        """Tạo danh mục"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required_fields = ['name', 'code']
            for field in required_fields:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name': data.get('name'),
                'name_en': data.get('name_en'),
                'code': data.get('code'),
                'description': data.get('description'),
                'description_en': data.get('description_en'),
                'sequence': data.get('sequence'),
                'active': data.get('active', True),
            }
            category = request.env['physical.gift.category'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': category.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/categories/<int:category_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_category(self, category_id, **kwargs):
        """Cập nhật danh mục"""
        try:
            category = request.env['physical.gift.category'].sudo().browse(category_id)
            if not category.exists():
                return json.dumps({'success': False, 'error': 'Danh mục không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name', 'name_en', 'code', 'description', 'description_en', 'sequence', 'active']
            update_vals = {k: data.get(k) for k in allowed if k in data}
            if update_vals:
                category.write(update_vals)
            return json.dumps({'success': True, 'data': {'id': category.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/categories/<int:category_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_category(self, category_id, **kwargs):
        """Xoá danh mục"""
        try:
            category = request.env['physical.gift.category'].sudo().browse(category_id)
            if not category.exists():
                return json.dumps({'success': False, 'error': 'Danh mục không tồn tại'}, ensure_ascii=False)
            category.unlink()
            return json.dumps({'success': True, 'data': {'id': category_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)