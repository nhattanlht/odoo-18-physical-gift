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
            
            # Tạo domain filter
            domain = [('active', '=', True)]
            
            # Tìm kiếm theo tên
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs.get('name')))
            
            # Lấy dữ liệu
            shipping_units = request.env['physical.gift.shipping.unit'].sudo().search(
                domain, 
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
                    'active': unit.active,
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