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
            
            # Filter theo state
            if kwargs.get('state'):
                domain.append(('state', '=', kwargs.get('state')))
            
            # Lấy dữ liệu
            programs = request.env['physical.gift.program'].sudo().search(
                domain, 
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
                    'state': program.state,
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