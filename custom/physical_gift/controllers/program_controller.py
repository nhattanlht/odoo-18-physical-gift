# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class ProgramController(http.Controller):
    """API Controller cho Physical Gift Program"""
    
    @http.route('/api/physical-gift/programs', type='http', auth='public', methods=['GET'], csrf=False)
    def get_programs(self, **kwargs):
        """Lấy danh sách chương trình"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Tạo domain filter
            domain = []
            
            # Filter theo brand_redeem_id
            if kwargs.get('brand_redeem_id'):
                domain.append(('brand_redeem_id', '=', int(kwargs.get('brand_redeem_id'))))
            
            # Lấy dữ liệu
            programs = request.env['physical.gift.program'].sudo().search(
                [],
                limit=limit, 
                offset=offset,
                order='name_vi'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for program in programs:
                data.append({
                    'id': program.id,
                    'name_vi': program.name_vi,
                    'name_en': program.name_en,
                    'company_id': program.company_id.id if program.company_id else None,
                    'company_name': program.company_id.name if program.company_id else None,
                    'logo': program.logo,
                    'order_creator_id': program.order_creator_id.id if program.order_creator_id else None,
                    'order_creator_name': program.order_creator_id.name if program.order_creator_id else None,
                    'brand_redeem_id': program.brand_redeem_id.id if program.brand_redeem_id else None,
                    'brand_redeem_name': program.brand_redeem_id.name if program.brand_redeem_id else None,
                    'store_redeem_id': program.store_redeem_id.id if program.store_redeem_id else None,
                    'store_redeem_name': program.store_redeem_id.name if program.store_redeem_id else None,
                    'bill_number': program.bill_number,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(programs)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 

    @http.route('/api/physical-gift/programs', type='http', auth='public', methods=['POST'], csrf=False)
    def create_program(self, **kwargs):
        """Tạo chương trình"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required = ['name_vi', 'name_en', 'company_id', 'order_creator_id', 'brand_redeem_id', 'store_redeem_id']
            for field in required:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name_vi': data.get('name_vi'),
                'name_en': data.get('name_en'),
                'company_id': int(data.get('company_id')),
                'order_creator_id': int(data.get('order_creator_id')),
                'brand_redeem_id': int(data.get('brand_redeem_id')),
                'store_redeem_id': int(data.get('store_redeem_id')),
                'bill_number': data.get('bill_number'),
                'creator_id': int(data.get('creator_id')) if data.get('creator_id') else request.env.user.id,
                'active': data.get('active', True),
                'description': data.get('description'),
                'start_date': data.get('start_date'),
                'end_date': data.get('end_date'),
                'category_ids': [(6, 0, list(map(int, data.get('category_ids', []))))],
                'logo': data.get('logo'),
            }
            program = request.env['physical.gift.program'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': program.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/programs/<int:program_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_program(self, program_id, **kwargs):
        """Cập nhật chương trình"""
        try:
            program = request.env['physical.gift.program'].sudo().browse(program_id)
            if not program.exists():
                return json.dumps({'success': False, 'error': 'Chương trình không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name_vi', 'name_en', 'company_id', 'order_creator_id', 'brand_redeem_id', 'store_redeem_id',
                       'bill_number', 'creator_id', 'active', 'description', 'start_date', 'end_date', 'category_ids', 'logo']
            vals = {}
            for k in allowed:
                if k in data:
                    if k in ['company_id', 'order_creator_id', 'brand_redeem_id', 'store_redeem_id', 'creator_id']:
                        vals[k] = int(data[k]) if data[k] else False
                    elif k == 'category_ids':
                        vals[k] = [(6, 0, list(map(int, data.get('category_ids', []))))]
                    else:
                        vals[k] = data[k]

            if vals:
                program.write(vals)
            return json.dumps({'success': True, 'data': {'id': program.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/programs/<int:program_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_program(self, program_id, **kwargs):
        """Xoá chương trình"""
        try:
            program = request.env['physical.gift.program'].sudo().browse(program_id)
            if not program.exists():
                return json.dumps({'success': False, 'error': 'Chương trình không tồn tại'}, ensure_ascii=False)
            program.unlink()
            return json.dumps({'success': True, 'data': {'id': program_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)