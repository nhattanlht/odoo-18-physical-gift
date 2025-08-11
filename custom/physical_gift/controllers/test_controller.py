# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json


class TestController(http.Controller):
    """Test Controller để kiểm tra API"""
    
    @http.route('/api/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_api(self, **kwargs):
        """Test API endpoint"""
        try:
            return json.dumps({
                'success': True,
                'message': 'API hoạt động bình thường!',
                'data': {
                    'test': 'Hello from Physical Gift API'
                }
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
    
    @http.route('/api/physical-gift/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_physical_gift(self, **kwargs):
        """Test Physical Gift API"""
        try:
            return json.dumps({
                'success': True,
                'message': 'Physical Gift API hoạt động!',
                'data': {
                    'module': 'physical_gift',
                    'status': 'active'
                }
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False) 