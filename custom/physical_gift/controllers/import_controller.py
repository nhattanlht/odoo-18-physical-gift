# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class ImportController(http.Controller):
    """API Controller cho Physical Gift Import (Phiếu nhập hàng) - CRUD tối giản"""

    def _serialize_import_brief(self, rec):
        return {
            'id': rec.id,
            'name': rec.name,
            'import_date': rec.import_date.strftime('%Y-%m-%d') if rec.import_date else None,
            'supplier_id': rec.supplier_id.id if rec.supplier_id else None,
            'supplier_name': rec.supplier_id.name if rec.supplier_id else None,
            'program_id': rec.program_id.id if rec.program_id else None,
            'program_name': getattr(rec.program_id, 'name_vi', None) or (rec.program_id.name if rec.program_id else None),
            'state': rec.state,
            'notes': rec.notes,
            'line_count': rec.line_count,
        }

    def _serialize_import_detail(self, rec):
        # Cho phép lấy chi tiết nếu cần (đọc) như một số controller khác có detail
        data = self._serialize_import_brief(rec)
        data['lines'] = [
            {
                'id': line.id,
                'item_id': line.item_id.id if line.item_id else None,
                'item_name': line.item_id.name if line.item_id else None,
                'sku': line.sku,
                'import_quantity': line.import_quantity,
                'export_return_quantity': line.export_return_quantity,
                'import_price_excl_vat': line.import_price_excl_vat,
                'sale_price_incl_vat': line.sale_price_incl_vat,
                'vat_percentage': line.vat_percentage,
                'points': line.points,
            }
            for line in rec.line_ids
        ]
        return data

    # -------------------- List (Read) -------------------- #
    @http.route('/api/physical-gift/imports', type='http', auth='public', methods=['GET'], csrf=False)
    def list_imports(self, **kwargs):
        try:
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))

            domain = []
            if kwargs.get('state'):
                domain.append(('state', '=', kwargs.get('state')))
            if kwargs.get('supplier_id'):
                domain.append(('supplier_id', '=', int(kwargs.get('supplier_id'))))
            if kwargs.get('program_id'):
                domain.append(('program_id', '=', int(kwargs.get('program_id'))))
            if kwargs.get('date_from'):
                domain.append(('import_date', '>=', kwargs.get('date_from')))
            if kwargs.get('date_to'):
                domain.append(('import_date', '<=', kwargs.get('date_to')))

            records = request.env['physical.gift.import'].sudo().search(domain, limit=limit, offset=offset, order='import_date desc, id desc')
            data = [self._serialize_import_brief(rec) for rec in records]
            return json.dumps({'success': True, 'data': data, 'total': len(records)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    # -------------------- Detail (Read, optional) -------------------- #
    @http.route('/api/physical-gift/imports/<int:import_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_import(self, import_id, **kwargs):
        try:
            rec = request.env['physical.gift.import'].sudo().browse(import_id)
            if not rec.exists():
                return json.dumps({'success': False, 'error': 'Phiếu nhập không tồn tại'}, ensure_ascii=False)
            return json.dumps({'success': True, 'data': self._serialize_import_detail(rec)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    # -------------------- Create -------------------- #
    @http.route('/api/physical-gift/imports', type='http', auth='public', methods=['POST'], csrf=False)
    def create_import(self, **kwargs):
        try:
            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            required_fields = ['supplier_id', 'program_id']
            for field in required_fields:
                if not data.get(field):
                    return json.dumps({'success': False, 'error': f'Trường {field} là bắt buộc'}, ensure_ascii=False)

            vals = {
                'name': data.get('name') or 'New',
                'import_date': data.get('import_date'),
                'supplier_id': int(data.get('supplier_id')),
                'program_id': int(data.get('program_id')),
                'notes': data.get('notes'),
            }

            # Cho phép tạo nhanh line_ids nếu client gửi kèm, nhưng không bắt buộc
            if data.get('lines'):
                vals['line_ids'] = [
                    (0, 0, {
                        'item_id': int(line['item_id']) if line.get('item_id') else False,
                        'sku': line.get('sku'),
                        'import_quantity': int(line.get('import_quantity', 1)),
                        'export_return_quantity': int(line.get('export_return_quantity', 0)),
                        'import_price_excl_vat': float(line.get('import_price_excl_vat', 0.0)),
                        'sale_price_incl_vat': float(line.get('sale_price_incl_vat', 0.0)),
                        'vat_percentage': float(line.get('vat_percentage', 0.0)),
                        'points': int(line.get('points', 0)),
                    }) for line in data['lines']
                ]

            rec = request.env['physical.gift.import'].sudo().create(vals)
            return json.dumps({'success': True, 'data': {'id': rec.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    # -------------------- Update -------------------- #
    @http.route('/api/physical-gift/imports/<int:import_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_import(self, import_id, **kwargs):
        try:
            rec = request.env['physical.gift.import'].sudo().browse(import_id)
            if not rec.exists():
                return json.dumps({'success': False, 'error': 'Phiếu nhập không tồn tại'}, ensure_ascii=False)

            data = request.httprequest.get_json()
            if not data:
                return json.dumps({'success': False, 'error': 'Dữ liệu không hợp lệ'}, ensure_ascii=False)

            allowed = ['name', 'import_date', 'supplier_id', 'program_id', 'notes', 'state']
            vals = {k: data.get(k) for k in allowed if k in data}
            if 'supplier_id' in vals:
                vals['supplier_id'] = int(vals['supplier_id']) if vals['supplier_id'] else False
            if 'program_id' in vals:
                vals['program_id'] = int(vals['program_id']) if vals['program_id'] else False

            if vals:
                rec.write(vals)
            return json.dumps({'success': True, 'data': {'id': rec.id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

    # -------------------- Delete -------------------- #
    @http.route('/api/physical-gift/imports/<int:import_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_import(self, import_id, **kwargs):
        try:
            rec = request.env['physical.gift.import'].sudo().browse(import_id)
            if not rec.exists():
                return json.dumps({'success': False, 'error': 'Phiếu nhập không tồn tại'}, ensure_ascii=False)
            rec.unlink()
            return json.dumps({'success': True, 'data': {'id': import_id}}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)