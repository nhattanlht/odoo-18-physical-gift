# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class BrandController(http.Controller):
    """API Controller cho Physical Gift Brand"""
    
    @http.route('/api/physical-gift/brands', type='http', auth='public', methods=['GET'], csrf=False)
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

    @http.route('/api/physical-gift/brands', type='http', auth='public', methods=['POST'], csrf=False)
    def create_brand(self, **kwargs):
        """Tạo thương hiệu mới"""
        try:
            data = request.httprequest.get_json()

            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required_fields = ['name', 'code']
            for field in required_fields:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            create_vals = {
                'name': data.get('name'),
                'name_en': data.get('name_en'),
                'code': data.get('code'),
                'contact_person': data.get('contact_person'),
                'phone': data.get('phone'),
                'email': data.get('email'),
                'address': data.get('address'),
                'website': data.get('website'),
                'description': data.get('description'),
                'partnership_date': data.get('partnership_date'),
                'contract_number': data.get('contract_number'),
                'commission_rate': data.get('commission_rate'),
                'sequence': data.get('sequence'),
                'active': data.get('active', True),
                'logo': data.get('logo'),
            }

            brand = request.env['physical.gift.brand'].sudo().create(create_vals)

            return json.dumps({'success': True, 'data': {'id': brand.id}}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/brands/<int:brand_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_brand(self, brand_id, **kwargs):
        """Cập nhật thương hiệu"""
        try:
            brand = request.env['physical.gift.brand'].sudo().browse(brand_id)
            if not brand.exists():
                return json.dumps({'success': False, 'error': 'Thương hiệu không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed_fields = ['name', 'name_en', 'code', 'contact_person', 'phone', 'email', 'address',
                              'website', 'description', 'partnership_date', 'contract_number',
                              'commission_rate', 'sequence', 'active', 'logo']
            update_vals = {k: data.get(k) for k in allowed_fields if k in data}

            if update_vals:
                brand.write(update_vals)

            return json.dumps({'success': True, 'data': {'id': brand.id}}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    @http.route('/api/physical-gift/brands/<int:brand_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_brand(self, brand_id, **kwargs):
        """Xoá thương hiệu"""
        try:
            brand = request.env['physical.gift.brand'].sudo().browse(brand_id)
            if not brand.exists():
                return json.dumps({'success': False, 'error': 'Thương hiệu không tồn tại'}, ensure_ascii=False)

            brand.unlink()
            return json.dumps({'success': True, 'data': {'id': brand_id}}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)