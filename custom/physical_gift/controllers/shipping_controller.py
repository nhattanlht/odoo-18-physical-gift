# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class ShippingController(http.Controller):
    """API Controller cho Physical Gift Shipping Unit"""
    
    @http.route('/api/physical-gift/shipping-units', type='http', auth='public', methods=['GET'], csrf=False)
    def get_shipping_units(self, **kwargs):
        """Lấy danh sách đơn vị vận chuyển"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Lấy dữ liệu
            shipping_units = request.env['physical.gift.shipping.unit'].sudo().search(
                [],
                limit=limit,
                offset=offset,
                order='name'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for unit in shipping_units:
                data.append({
                    'id': unit.id,
                    'name': unit.name,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(shipping_units)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 

    @http.route('/api/physical-gift/shipping-units', type='http', auth='public', methods=['POST'], csrf=False)
    def create_shipping_unit(self, **kwargs):
        """Tạo đơn vị vận chuyển"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required = ['name', 'code']
            for field in required:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name': data.get('name'),
                'code': data.get('code'),
                'state': data.get('state', 'active'),
                'description': data.get('description'),
                'contact_info': data.get('contact_info'),
                'website': data.get('website'),
                'phone': data.get('phone'),
                'email': data.get('email'),
                'address': data.get('address'),
                'logo': data.get('logo'),
            }
            unit = request.env['physical.gift.shipping.unit'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': unit.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/shipping-units/<int:unit_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_shipping_unit(self, unit_id, **kwargs):
        """Cập nhật đơn vị vận chuyển"""
        try:
            unit = request.env['physical.gift.shipping.unit'].sudo().browse(unit_id)
            if not unit.exists():
                return json.dumps({'success': False, 'error': 'Đơn vị vận chuyển không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name', 'code', 'state', 'description', 'contact_info', 'website', 'phone', 'email', 'address', 'logo']
            vals = {k: data.get(k) for k in allowed if k in data}
            if vals:
                unit.write(vals)
            return json.dumps({'success': True, 'data': {'id': unit.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/shipping-units/<int:unit_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_shipping_unit(self, unit_id, **kwargs):
        """Xoá đơn vị vận chuyển"""
        try:
            unit = request.env['physical.gift.shipping.unit'].sudo().browse(unit_id)
            if not unit.exists():
                return json.dumps({'success': False, 'error': 'Đơn vị vận chuyển không tồn tại'}, ensure_ascii=False)
            unit.unlink()
            return json.dumps({'success': True, 'data': {'id': unit_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)