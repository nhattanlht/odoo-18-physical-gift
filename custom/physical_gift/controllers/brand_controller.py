# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class BrandController(http.Controller):
    """API Controller cho Physical Gift Brand"""
    
    @http.route('/api/physical-gift/brands', type='http', auth='none', methods=['GET'], csrf=False)
    def get_brands(self, **kwargs):
        """Lấy danh sách thương hiệu"""
        try:
            # Lấy tham số filter
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            # Tạo domain filter
            domain = [('active', '=', True)]
            
            # Tìm kiếm theo tên
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs.get('name')))
            
            # Tìm kiếm theo mã
            if kwargs.get('code'):
                domain.append(('code', 'ilike', kwargs.get('code')))
            
            # Lấy dữ liệu
            brands = request.env['physical.gift.brand'].sudo().search(
                domain, 
                limit=limit, 
                offset=offset,
                order='sequence, name'
            )
            
            # Chuẩn bị dữ liệu trả về
            data = []
            for brand in brands:
                data.append({
                    'name': brand.name,
                    'name_en': brand.name_en,
                    'code': brand.code,
                    'contact_person': brand.contact_person,
                    'phone': brand.phone,
                    'email': brand.email,
                    'address': brand.address,
                    'website': brand.website,
                    'description': brand.description,
                    'partnership_date': brand.partnership_date.strftime('%Y-%m-%d') if brand.partnership_date else None,
                    'contract_number': brand.contract_number,
                    'commission_rate': brand.commission_rate,
                    'store_count': brand.store_count,
                    'program_count': brand.program_count,
                    'active': brand.active,
                })
            
            return json.dumps({
                'success': True,
                'data': data,
                'total': len(brands)
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
    
    @http.route('/api/physical-gift/brands/<int:brand_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_brand_detail(self, brand_id, **kwargs):
        """Lấy chi tiết thương hiệu theo ID"""
        try:
            brand = request.env['physical.gift.brand'].sudo().browse(brand_id)
            
            if not brand.exists():
                return json.dumps({
                    'success': False,
                    'error': 'Thương hiệu không tồn tại'
                }, ensure_ascii=False)
            
            # Chuẩn bị dữ liệu trả về
            data = {
                'id': brand.id,
                'name': brand.name,
                'name_en': brand.name_en,
                'code': brand.code,
                'contact_person': brand.contact_person,
                'phone': brand.phone,
                'email': brand.email,
                'address': brand.address,
                'website': brand.website,
                'description': brand.description,
                'logo': brand.logo,
                'sequence': brand.sequence,
                'partnership_date': brand.partnership_date.strftime('%Y-%m-%d') if brand.partnership_date else None,
                'contract_number': brand.contract_number,
                'commission_rate': brand.commission_rate,
                'store_count': brand.store_count,
                'program_count': brand.program_count,
                'active': brand.active,
                'status_display': brand.status_display,
                'stores': [{'id': store.id, 'name': store.name} for store in brand.store_ids],
                'programs': [{'id': program.id, 'name_vi': program.name_vi, 'name_en': program.name_en} for program in brand.program_ids],
                'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in brand.supplier_ids],
            }
            
            return json.dumps({
                'success': True,
                'data': data
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 