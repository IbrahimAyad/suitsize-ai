#!/usr/bin/env python3
"""
Comprehensive test suite for KCTmenswear Integration
Tests all major functionality including wedding party integration
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kctmenswear_integration import (
    KCTmenswearIntegration, KCTOrderStatus, KCTProductType,
    KCTOrderItem, KCTWeddingOrder
)
from wedding_sizing_engine import WeddingSizingEngine, WeddingRole, WeddingStyle, WeddingPartyMember, WeddingDetails
from wedding_group_coordination import WeddingGroup, GroupConsistencyAnalyzer

def test_kct_integration():
    """Test KCTmenswear integration functionality"""
    print("🧪 Testing KCTmenswear Integration...")
    
    # Initialize integration
    kct = KCTmenswearIntegration()
    
    # Test 1: Basic API connectivity
    print("  📡 Testing API connectivity...")
    try:
        status = kct.get_api_status()
        print(f"  ✅ API Status: {status}")
    except Exception as e:
        print(f"  ❌ API connectivity failed: {e}")
        return False
    
    # Test 2: Wedding party synchronization
    print("  👥 Testing wedding party sync...")
    try:
        # Create sample wedding party data
        wedding_members = [
            WeddingPartyMember(
                name="John Smith",
                role=WeddingRole.GROOM,
                measurements={"chest": 42, "waist": 32, "height": 70},
                preferences={"style": WeddingStyle.CLASSIC, "color": "navy"}
            ),
            WeddingPartyMember(
                name="Mike Johnson",
                role=WeddingRole.BEST_MAN,
                measurements={"chest": 40, "waist": 30, "height": 68},
                preferences={"style": WeddingStyle.MODERN, "color": "navy"}
            )
        ]
        
        wedding_details = WeddingDetails(
            wedding_date=datetime.now() + timedelta(days=90),
            venue="Grand Ballroom",
            color_scheme="navy and gold",
            theme="elegant"
        )
        
        sync_result = kct.sync_wedding_party(wedding_members, wedding_details)
        print(f"  ✅ Wedding sync result: {sync_result.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"  ❌ Wedding party sync failed: {e}")
        return False
    
    # Test 3: Bulk order creation
    print("  📦 Testing bulk order creation...")
    try:
        order_items = [
            KCTOrderItem(
                member_name="John Smith",
                product_type=KCTProductType.SUIT,
                size_data={"chest": 42, "waist": 32, "jacket_size": "42R"},
                quantity=1
            ),
            KCTOrderItem(
                member_name="Mike Johnson",
                product_type=KCTProductType.SUIT,
                size_data={"chest": 40, "waist": 30, "jacket_size": "40R"},
                quantity=1
            )
        ]
        
        wedding_order = KCTWeddingOrder(
            wedding_party_id="wedding_001",
            customer_info={"name": "Jane Doe", "email": "jane@example.com"},
            order_items=order_items,
            estimated_delivery=datetime.now() + timedelta(days=60),
            special_instructions="Rush order for wedding"
        )
        
        order_result = kct.create_bulk_order(wedding_order)
        print(f"  ✅ Bulk order created: {order_result.get('order_id', 'unknown')}")
        
    except Exception as e:
        print(f"  ❌ Bulk order creation failed: {e}")
        return False
    
    # Test 4: Order tracking
    print("  📊 Testing order tracking...")
    try:
        if 'order_result' in locals():
            order_id = order_result.get('order_id')
            if order_id:
                tracking_info = kct.track_order(order_id)
                print(f"  ✅ Order tracking: {tracking_info.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"  ❌ Order tracking failed: {e}")
        return False
    
    # Test 5: Inventory checking
    print("  📋 Testing inventory checking...")
    try:
        inventory = kct.check_inventory(
            product_type=KCTProductType.SUIT,
            size_range={"chest": (38, 46), "waist": (28, 36)},
            color_preferences=["navy", "black"]
        )
        print(f"  ✅ Inventory check completed: {len(inventory.get('available_items', []))} items available")
        
    except Exception as e:
        print(f"  ❌ Inventory checking failed: {e}")
        return False
    
    print("🎉 KCTmenswear Integration tests completed successfully!")
    return True

def test_wedding_sizing_integration():
    """Test integration between wedding sizing and KCT"""
    print("\n🧪 Testing Wedding Sizing + KCT Integration...")
    
    try:
        # Initialize engines
        wedding_engine = WeddingSizingEngine()
        kct = KCTmenswearIntegration()
        consistency_analyzer = GroupConsistencyAnalyzer()
        
        # Create wedding party
        wedding_group = WeddingGroup(
            wedding_id="integration_test_001",
            wedding_details=WeddingDetails(
                wedding_date=datetime.now() + timedelta(days=120),
                venue="Test Venue",
                color_scheme="navy and white",
                theme="traditional"
            )
        )
        
        # Add members with realistic measurements
        members = [
            WeddingPartyMember("Groom Test", WeddingRole.GROOM, 
                             {"chest": 44, "waist": 34, "height": 72}, 
                             {"style": WeddingStyle.CLASSIC, "color": "navy"}),
            WeddingPartyMember("Best Man Test", WeddingRole.BEST_MAN, 
                             {"chest": 42, "waist": 32, "height": 70}, 
                             {"style": WeddingStyle.MODERN, "color": "navy"}),
            WeddingPartyMember("Groomsman 1", WeddingRole.GROOMSMAN, 
                             {"chest": 40, "waist": 30, "height": 68}, 
                             {"style": WeddingStyle.TRENDY, "color": "navy"}),
            WeddingPartyMember("Groomsman 2", WeddingRole.GROOMSMAN, 
                             {"chest": 46, "waist": 36, "height": 74}, 
                             {"style": WeddingStyle.CLASSIC, "color": "navy"})
        ]
        
        for member in members:
            wedding_group.add_member(member)
        
        # Test sizing recommendations
        print("  📏 Testing size recommendations...")
        sizing_results = []
        for member in members:
            result = wedding_engine.recommend_size(member)
            sizing_results.append(result)
            print(f"    ✅ {member.name}: {result.get('recommended_size', 'unknown')}")
        
        # Test group consistency
        print("  🎯 Testing group consistency...")
        consistency_score = consistency_analyzer.calculate_group_consistency(wedding_group)
        print(f"    ✅ Group consistency score: {consistency_score:.1f}%")
        
        # Test bulk order preparation
        print("  📦 Testing bulk order preparation...")
        order_items = []
        for i, (member, sizing) in enumerate(zip(members, sizing_results)):
            order_item = KCTOrderItem(
                member_name=member.name,
                product_type=KCTProductType.SUIT,
                size_data=sizing.get('size_details', {}),
                quantity=1
            )
            order_items.append(order_item)
        
        # Calculate group savings
        savings = kct.calculate_group_discount(len(order_items))
        print(f"    ✅ Group discount: {savings:.1f}%")
        
        print("🎉 Wedding Sizing + KCT Integration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Wedding Sizing + KCT Integration test failed: {e}")
        return False

def run_comprehensive_tests():
    """Run all integration tests"""
    print("🚀 Starting Comprehensive KCTmenswear Integration Tests")
    print("=" * 60)
    
    start_time = time.time()
    
    # Test KCT Integration
    kct_success = test_kct_integration()
    
    # Test Wedding Sizing Integration
    wedding_success = test_wedding_sizing_integration()
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"  KCT Integration: {'✅ PASS' if kct_success else '❌ FAIL'}")
    print(f"  Wedding Integration: {'✅ PASS' if wedding_success else '❌ FAIL'}")
    print(f"  Overall: {'✅ ALL TESTS PASSED' if kct_success and wedding_success else '❌ SOME TESTS FAILED'}")
    print(f"  Duration: {duration:.2f} seconds")
    print("=" * 60)
    
    return kct_success and wedding_success

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)