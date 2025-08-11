# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json
from datetime import datetime


class OrderController(http.Controller):
    """API Controller cho Physical Gift Order"""
    
    @http.route('/api/physical-gift/orders', type='http', auth='public', methods=['GET'], csrf=False)
    def get_orders(self, **kwargs):
        """Lấy danh sách đơn hàng"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Tạo domain filter
            domain = []
            
            # Filter theo program_id
            if kwargs.get('program_id'):
                domain.append(('program_id', '=', int(kwargs.get('program_id'))))
            
            # Filter theo order_status
            if kwargs.get('order_status'):
                domain.append(('order_status', '=', kwargs.get('order_status')))
            
            # Filter theo payment_status
            if kwargs.get('payment_status'):
                domain.append(('payment_status', '=', kwargs.get('payment_status')))
            
            # Lấy dữ liệu
            orders = request.env['physical.gift.order'].sudo().search(
                domain, 
                limit=limit, 
                offset=offset,
                order='create_date desc'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for order in orders:
                data.append({
                    'id': order.id,
                    'program_id': order.program_id.id if order.program_id else None,
                    'program_name': order.program_id.name_vi if order.program_id else None,
                    'recipient_name': order.recipient_name,
                    'recipient_phone': order.recipient_phone,
                    'total_order_value': order.total_order_value,
                    'voucher_code': order.voucher_code,
                    'shipping_unit_id': order.shipping_unit_id.id if order.shipping_unit_id else None,
                    'shipping_unit_name': order.shipping_unit_id.name if order.shipping_unit_id else None,
                    'waybill_code': order.waybill_code,
                    'payment_gateway': order.payment_gateway,
                    'payment_status': order.payment_status,
                    'transaction_code': order.transaction_code,
                    'product_type': order.product_type,
                    'order_time': order.order_time.strftime('%Y-%m-%d %H:%M:%S') if order.order_time else None,
                    'create_date': order.create_date.strftime('%Y-%m-%d %H:%M:%S') if order.create_date else None,
                    'order_status': order.order_status,
                    'error_content': order.error_content,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(orders)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
    
    @http.route('/api/physical-gift/orders', type='http', auth='public', methods=['POST'], csrf=False)
    def create_order(self, **kwargs):
        """Tạo đơn hàng mới"""
        try:
            # Lấy dữ liệu từ request
            data = request.httprequest.get_json()
            
            if not data:
                return json.dumps({
                    'success': False,
                    'error': 'Dữ liệu không hợp lệ'
                }, ensure_ascii=False)
            
            # Validate dữ liệu bắt buộc
            required_fields = ['program_id', 'recipient_name', 'recipient_phone']
            for field in required_fields:
                if not data.get(field):
                    return json.dumps({
                        'success': False,
                        'error': f'Trường {field} là bắt buộc'
                    }, ensure_ascii=False)
            
            # Tạo đơn hàng
            order_data = {
                'program_id': int(data['program_id']),
                'recipient_name': data['recipient_name'],
                'recipient_phone': data['recipient_phone'],
                'total_order_value': data.get('total_order_value', 0.0),
                'voucher_code': data.get('voucher_code'),
                'shipping_unit_id': int(data['shipping_unit_id']) if data.get('shipping_unit_id') else None,
                'waybill_code': data.get('waybill_code'),
                'payment_gateway': data.get('payment_gateway'),
                'payment_status': data.get('payment_status', 'pending'),
                'transaction_code': data.get('transaction_code'),
                'product_type': data.get('product_type'),
                'order_status': data.get('order_status', 'draft'),
                'error_content': data.get('error_content'),
            }
            
            # Xử lý order_time nếu có
            if data.get('order_time'):
                try:
                    order_data['order_time'] = datetime.strptime(data['order_time'], '%Y-%m-%d %H:%M:%S')
                except:
                    order_data['order_time'] = datetime.now()
            
            # Tạo đơn hàng
            order = request.env['physical.gift.order'].sudo().create(order_data)
            
            return json.dumps({
                'success': True,
                'data': {
                    'id': order.id,
                    'message': 'Tạo đơn hàng thành công'
                }
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
    
    @http.route('/api/physical-gift/orders/<int:order_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_order(self, order_id, **kwargs):
        """Cập nhật đơn hàng"""
        try:
            # Kiểm tra đơn hàng tồn tại
            order = request.env['physical.gift.order'].sudo().browse(order_id)
            
            if not order.exists():
                return json.dumps({
                    'success': False,
                    'error': 'Đơn hàng không tồn tại'
                }, ensure_ascii=False)
            
            # Lấy dữ liệu từ request
            data = request.httprequest.get_json()
            
            if not data:
                return json.dumps({
                    'success': False,
                    'error': 'Dữ liệu không hợp lệ'
                }, ensure_ascii=False)
            
            # Chuẩn bị dữ liệu cập nhật
            update_data = {}
            
            # Các trường có thể cập nhật
            allowed_fields = [
                'recipient_name', 'recipient_phone', 'total_order_value',
                'voucher_code', 'shipping_unit_id', 'waybill_code',
                'payment_gateway', 'payment_status', 'transaction_code',
                'product_type', 'order_status', 'error_content'
            ]
            
            for field in allowed_fields:
                if field in data:
                    if field == 'shipping_unit_id' and data[field]:
                        update_data[field] = int(data[field])
                    else:
                        update_data[field] = data[field]
            
            # Xử lý order_time nếu có
            if data.get('order_time'):
                try:
                    update_data['order_time'] = datetime.strptime(data['order_time'], '%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            # Cập nhật đơn hàng
            order.write(update_data)
            
            return json.dumps({
                'success': True,
                'data': {
                    'id': order.id,
                    'message': 'Cập nhật đơn hàng thành công'
                }
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 