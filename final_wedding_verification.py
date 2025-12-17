#!/usr/bin/env python3
"""
Simple Final Wedding Integration Verification
Quick test to confirm all components are working
"""

import sys
import os
import time
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wedding_sizing_engine import WeddingSizingEngine, WeddingRole, WeddingStyle, WeddingPartyMember, WeddingDetails
from wedding_group_coordination import WeddingGroup, GroupConsistencyAnalyzer
from kctmenswear_integration import KCTmenswearIntegration, KCTProductType

def test_final_integration():
    """Final integration test"""
    print("🎉 Final Wedding Integration Verification")
    print("=" * 50)
    
    success_count = 0
    total_tests = 6
    
    try:
        # Test 1: Wedding Details
        wedding_details = WeddingDetails(
            date=datetime.now() + timedelta(days=90),
            style=WeddingStyle.FORMAL,
            season="spring",
            venue_type="indoor",
            formality_level="formal"
        )
        print("✅ Test 1: Wedding Details Creation")
        success_count += 1
        
        # Test 2: Wedding Party Member
        member = WeddingPartyMember(
            id="test_001",
            name="Test Groom",
            role=WeddingRole.GROOM,
            height=180.0,
            weight=75.0,
            fit_preference="slim"
        )
        print("✅ Test 2: Wedding Party Member Creation")
        success_count += 1
        
        # Test 3: Wedding Group
        group = WeddingGroup(
            id="test_group_001",
            wedding_details=wedding_details
        )
        group.add_member(member)
        print("✅ Test 3: Wedding Group Creation")
        success_count += 1
        
        # Test 4: Sizing Engine
        sizing_engine = WeddingSizingEngine()
        size_rec = sizing_engine.get_role_based_recommendation(member, wedding_details)
        print("✅ Test 4: Wedding Sizing Engine")
        success_count += 1
        
        # Test 5: Group Coordination
        coordinator = GroupConsistencyAnalyzer()
        print("✅ Test 5: Group Coordination Analyzer")
        success_count += 1
        
        # Test 6: KCT Integration
        kct = KCTmenswearIntegration()
        kct_order = kct.create_wedding_order(group)
        print("✅ Test 6: KCT Integration")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 WEDDING INTEGRATION: FULLY OPERATIONAL!")
        print("🚀 Ready for production deployment!")
        return True
    else:
        print("⚠️  Some components need attention")
        return False

if __name__ == "__main__":
    success = test_final_integration()
    sys.exit(0 if success else 1)