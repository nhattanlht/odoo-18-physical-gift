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

    @http.route('/api/physical-gift/items', type='http', auth='public', methods=['POST'], csrf=False)
    def create_item(self, **kwargs):
        """Tạo sản phẩm quà tặng"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required = ['name']
            for field in required:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name': data.get('name'),
                'brand_id': int(data['brand_id']) if data.get('brand_id') else False,
                'category_id': int(data['category_id']) if data.get('category_id') else False,
                'supplier_id': int(data['supplier_id']) if data.get('supplier_id') else False,
                'quantity': data.get('quantity', 1),
                'unit_price': data.get('unit_price', 0.0),
                'image': data.get('image'),
                'active': data.get('active', True),
            }
            item = request.env['physical.gift.item'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': item.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/items/<int:item_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_item(self, item_id, **kwargs):
        """Cập nhật sản phẩm"""
        try:
            item = request.env['physical.gift.item'].sudo().browse(item_id)
            if not item.exists():
                return json.dumps({'success': False, 'error': 'Sản phẩm không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name', 'brand_id', 'category_id', 'supplier_id', 'quantity', 'unit_price', 'image', 'active']
            vals = {}
            for k in allowed:
                if k in data:
                    if k in ['brand_id', 'category_id', 'supplier_id']:
                        vals[k] = int(data[k]) if data[k] else False
                    else:
                        vals[k] = data[k]

            if vals:
                item.write(vals)
            return json.dumps({'success': True, 'data': {'id': item.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/items/<int:item_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_item(self, item_id, **kwargs):
        """Xoá sản phẩm"""
        try:
            item = request.env['physical.gift.item'].sudo().browse(item_id)
            if not item.exists():
                return json.dumps({'success': False, 'error': 'Sản phẩm không tồn tại'}, ensure_ascii=False)
            item.unlink()
            return json.dumps({'success': True, 'data': {'id': item_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)