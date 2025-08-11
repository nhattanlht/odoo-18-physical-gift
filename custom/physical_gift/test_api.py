#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Physical Gift API endpoints
Usage: python test_api.py
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8069"  # Change this to your Odoo server URL
API_BASE = f"{BASE_URL}/api/physical-gift"

def test_api_endpoint(endpoint, method="GET", data=None, params=None):
    """Test an API endpoint"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        elif method == "PUT":
            response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"\n{'='*50}")
        print(f"Testing {method} {endpoint}")
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def main():
    """Main test function"""
    print("Physical Gift API Test Suite")
    print("="*50)
    
    # Test 1: Get all brands
    print("\n1. Testing GET /brands")
    test_api_endpoint("/brands")
    
    # Test 2: Get all categories
    print("\n2. Testing GET /categories")
    test_api_endpoint("/categories")
    
    # Test 3: Get all items
    print("\n3. Testing GET /items")
    test_api_endpoint("/items")
    
    # Test 4: Get items with filter
    print("\n4. Testing GET /items with filter")
    test_api_endpoint("/items", params={"brand_id": 1})
    
    # Test 5: Get all programs
    print("\n5. Testing GET /programs")
    test_api_endpoint("/programs")
    
    # Test 6: Get all orders
    print("\n6. Testing GET /orders")
    test_api_endpoint("/orders")
    
    # Test 7: Get all suppliers
    print("\n7. Testing GET /suppliers")
    test_api_endpoint("/suppliers")
    
    # Test 8: Get all shipping units
    print("\n8. Testing GET /shipping-units")
    test_api_endpoint("/shipping-units")
    
    # Test 9: Create a new order
    print("\n9. Testing POST /orders")
    order_data = {
        "program_id": 1,
        "recipient_name": "Test User",
        "recipient_phone": "0123456789",
        "total_order_value": 1000000,
        "voucher_code": "TEST001",
        "payment_gateway": "bank_transfer",
        "product_type": "physical"
    }
    success = test_api_endpoint("/orders", method="POST", data=order_data)
    
    # Test 10: Get brand detail (if brand exists)
    print("\n10. Testing GET /brands/1")
    test_api_endpoint("/brands/1")
    
    print("\n" + "="*50)
    print("API Test completed!")

if __name__ == "__main__":
    main() 