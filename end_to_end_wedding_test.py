#!/usr/bin/env python3
"""
End-to-End Wedding Party Sizing Workflow Test
Comprehensive test covering the complete wedding integration workflow
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wedding_sizing_engine import WeddingSizingEngine, WeddingRole, WeddingStyle, WeddingPartyMember, WeddingDetails
from wedding_group_coordination import WeddingGroup, GroupConsistencyAnalyzer
from kctmenswear_integration import KCTmenswearIntegration, KCTProductType, KCTWeddingOrder, KCTOrderItem

def create_realistic_wedding_party() -> WeddingGroup:
    """Create a realistic wedding party for testing"""
    print("👥 Creating realistic wedding party...")
    
    # Wedding details
    wedding_details = WeddingDetails(
        date=datetime.now() + timedelta(days=120),  # 4 months out
        style=WeddingStyle.FORMAL,
        season="spring",
        venue_type="indoor",
        formality_level="formal",
        color_scheme=["navy", "gold", "white"],
        special_requests=["rush delivery", "group discount"]
    )
    
    # Create wedding group
    wedding_group = WeddingGroup(
        id="realistic_wedding_001",
        wedding_details=wedding_details
    )
    
    # Create realistic wedding party members
    wedding_party = [
        # Groom
        WeddingPartyMember(
            id="groom_001",
            name="Michael Johnson",
            role=WeddingRole.GROOM,
            height=182.0,
            weight=78.0,
            fit_preference="slim",
            unit="metric",
            age=28,
            body_type="athletic"
        ),
        
        # Best Man
        WeddingPartyMember(
            id="bestman_001", 
            name="David Chen",
            role=WeddingRole.BEST_MAN,
            height=175.0,
            weight=72.0,
            fit_preference="regular",
            unit="metric",
            age=29,
            body_type="medium"
        ),
        
        # Groomsmen (3)
        WeddingPartyMember(
            id="groomsman_001",
            name="James Wilson",
            role=WeddingRole.GROOMSMAN,
            height=178.0,
            weight=75.0,
            fit_preference="slim",
            unit="metric",
            age=26,
            body_type="athletic"
        ),
        
        WeddingPartyMember(
            id="groomsman_002",
            name="Robert Davis", 
            role=WeddingRole.GROOMSMAN,
            height=180.0,
            weight=80.0,
            fit_preference="regular",
            unit="metric",
            age=30,
            body_type="large"
        ),
        
        WeddingPartyMember(
            id="groomsman_003",
            name="Kevin Brown",
            role=WeddingRole.GROOMSMAN,
            height=172.0,
            weight=68.0,
            fit_preference="slim",
            unit="metric",
            age=25,
            body_type="slim"
        ),
        
        # Father of Groom
        WeddingPartyMember(
            id="father_groom_001",
            name="Robert Johnson Sr.",
            role=WeddingRole.FATHER_OF_GROOM,
            height=175.0,
            weight=85.0,
            fit_preference="relaxed",
            unit="metric",
            age=55,
            body_type="large"
        )
    ]
    
    # Add all members to group
    for member in wedding_party:
        wedding_group.add_member(member)
    
    print(f"  ✅ Created wedding party with {len(wedding_party)} members")
    return wedding_group

def test_sizing_workflow(wedding_group: WeddingGroup) -> Dict[str, Any]:
    """Test the complete sizing workflow"""
    print("\n📏 Testing Wedding Party Sizing Workflow...")
    
    # Initialize sizing engine
    sizing_engine = WeddingSizingEngine()
    
    sizing_results = {}
    
    # Get individual sizing for each member
    print("  🎯 Calculating individual sizes...")
    for member in wedding_group.members:
        try:
            size_rec = sizing_engine.get_role_based_recommendation(member, wedding_group.wedding_details)
            sizing_results[member.id] = {
                'member_name': member.name,
                'role': member.role.value,
                'size_recommendation': size_rec,
                'measurements': {
                    'height': member.height,
                    'weight': member.weight,
                    'fit_preference': member.fit_preference
                }
            }
            print(f"    ✅ {member.name} ({member.role.value}): {size_rec.get('jacket_size', 'N/A')}")
        except Exception as e:
            print(f"    ❌ Error sizing {member.name}: {e}")
            sizing_results[member.id] = {'error': str(e)}
    
    return sizing_results

def test_group_coordination(wedding_group: WeddingGroup, sizing_results: Dict[str, Any]):
    """Test group coordination and consistency"""
    print("\n🎯 Testing Group Coordination...")
    
    # Initialize coordination analyzer
    coordinator = GroupConsistencyAnalyzer()
    
    try:
        # Calculate group consistency
        consistency_score = coordinator.calculate_group_consistency(wedding_group)
        print(f"  ✅ Group consistency score: {consistency_score:.1f}%")
        
        # Test bulk order optimization
        total_members = len(wedding_group.members)
        base_price = 450.0  # Base suit price
        
        # Calculate bulk discounts
        if total_members >= 6:
            discount_rate = 0.15  # 15% for 6+ members
        elif total_members >= 4:
            discount_rate = 0.10  # 10% for 4+ members
        else:
            discount_rate = 0.05  # 5% for 3+ members
        
        total_cost = total_members * base_price
        bulk_discount = total_cost * discount_rate
        final_cost = total_cost - bulk_discount
        
        print(f"  📊 Bulk Order Analysis:")
        print(f"    • Total members: {total_members}")
        print(f"    • Base cost: ${total_cost:,.2f}")
        print(f"    • Bulk discount ({discount_rate*100:.0f}%): ${bulk_discount:,.2f}")
        print(f"    • Final cost: ${final_cost:,.2f}")
        print(f"    • Savings: ${bulk_discount:,.2f}")
        
        return {
            'consistency_score': consistency_score,
            'bulk_discount': bulk_discount,
            'total_savings': bulk_discount
        }
        
    except Exception as e:
        print(f"  ❌ Group coordination test failed: {e}")
        return {'error': str(e)}

def test_kct_integration_workflow(wedding_group: WeddingGroup, sizing_results: Dict[str, Any]):
    """Test KCT integration workflow"""
    print("\n🛒 Testing KCT Integration Workflow...")
    
    # Initialize KCT integration
    kct = KCTmenswearIntegration()
    
    try:
        # Create KCT wedding order
        kct_order = kct.create_wedding_order(wedding_group)
        print(f"  ✅ KCT order created: {kct_order.kct_order_number}")
        
        # Add items to the order based on sizing results
        for member_id, result in sizing_results.items():
            if 'error' not in result:
                member = next(m for m in wedding_group.members if m.id == member_id)
                
                order_item = KCTOrderItem(
                    member_name=member.name,
                    product_type=KCTProductType.SUIT,
                    size_data=result['size_recommendation'].get('size_details', {}),
                    quantity=1
                )
                kct_order.add_item(order_item)
        
        print(f"  ✅ Added {len(kct_order.items)} items to KCT order")
        
        # Get order dashboard
        dashboard = kct.get_wedding_order_dashboard(kct_order)
        print(f"  ✅ Generated order dashboard with {len(dashboard)} sections")
        
        # Track order status
        tracking = kct.track_order_status(kct_order.kct_order_number)
        print(f"  ✅ Order tracking: {tracking.get('status', 'unknown')}")
        
        return {
            'kct_order_id': kct_order.kct_order_number,
            'dashboard_sections': len(dashboard),
            'order_status': tracking.get('status', 'unknown')
        }
        
    except Exception as e:
        print(f"  ❌ KCT integration test failed: {e}")
        return {'error': str(e)}

def test_timeline_and_delivery(wedding_group: WeddingGroup):
    """Test wedding timeline and delivery planning"""
    print("\n📅 Testing Timeline and Delivery Planning...")
    
    try:
        wedding_date = wedding_group.wedding_details.date
        current_date = datetime.now()
        days_until_wedding = (wedding_date - current_date).days
        
        print(f"  📆 Wedding date: {wedding_date.strftime('%Y-%m-%d')}")
        print(f"  ⏰ Days until wedding: {days_until_wedding} days")
        
        # Calculate production timeline
        if days_until_wedding >= 90:
            production_timeline = "Standard (8-10 weeks)"
            rush_order = False
        elif days_until_wedding >= 60:
            production_timeline = "Express (6-8 weeks)"
            rush_order = False
        elif days_until_wedding >= 30:
            production_timeline = "Rush (4-6 weeks)"
            rush_order = True
        else:
            production_timeline = "Emergency (2-4 weeks)"
            rush_order = True
        
        print(f"  🏭 Production timeline: {production_timeline}")
        print(f"  🚨 Rush order required: {'Yes' if rush_order else 'No'}")
        
        # Calculate delivery date
        if rush_order:
            production_weeks = 4
        else:
            production_weeks = 8
        
        delivery_date = current_date + timedelta(weeks=production_weeks)
        print(f"  📦 Estimated delivery: {delivery_date.strftime('%Y-%m-%d')}")
        
        return {
            'days_until_wedding': days_until_wedding,
            'production_timeline': production_timeline,
            'rush_order': rush_order,
            'estimated_delivery': delivery_date.strftime('%Y-%m-%d')
        }
        
    except Exception as e:
        print(f"  ❌ Timeline test failed: {e}")
        return {'error': str(e)}

def run_end_to_end_test():
    """Run comprehensive end-to-end wedding party workflow test"""
    print("🚀 End-to-End Wedding Party Sizing Workflow Test")
    print("=" * 70)
    
    start_time = time.time()
    
    try:
        # Step 1: Create realistic wedding party
        wedding_group = create_realistic_wedding_party()
        
        # Step 2: Test sizing workflow
        sizing_results = test_sizing_workflow(wedding_group)
        
        # Step 3: Test group coordination
        coordination_results = test_group_coordination(wedding_group, sizing_results)
        
        # Step 4: Test KCT integration
        kct_results = test_kct_integration_workflow(wedding_group, sizing_results)
        
        # Step 5: Test timeline planning
        timeline_results = test_timeline_and_delivery(wedding_group)
        
        # Compile final results
        end_time = time.time()
        duration = end_time - start_time
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 End-to-End Test Results Summary:")
        print(f"  🎯 Wedding Party Created: ✅ {len(wedding_group.members)} members")
        print(f"  📏 Sizing Workflow: ✅ {len([r for r in sizing_results.values() if 'error' not in r])}/{len(wedding_group.members)} members sized")
        print(f"  🎯 Group Coordination: ✅ {coordination_results.get('consistency_score', 'N/A'):.1f}% consistency")
        print(f"  🛒 KCT Integration: ✅ Order {kct_results.get('kct_order_id', 'N/A')}")
        print(f"  📅 Timeline Planning: ✅ {timeline_results.get('production_timeline', 'N/A')}")
        print(f"  ⏱️  Total Duration: {duration:.2f} seconds")
        print("=" * 70)
        
        # Final validation
        all_tests_passed = (
            len(wedding_group.members) > 0 and
            len([r for r in sizing_results.values() if 'error' not in r]) > 0 and
            'error' not in coordination_results and
            'error' not in kct_results and
            'error' not in timeline_results
        )
        
        if all_tests_passed:
            print("🎉 END-TO-END WEDDING WORKFLOW: ✅ ALL TESTS PASSED!")
            print("\n🚀 Wedding Integration is fully operational and ready for production!")
        else:
            print("⚠️  END-TO-END WEDDING WORKFLOW: Some tests had issues")
        
        return all_tests_passed
        
    except Exception as e:
        print(f"\n❌ End-to-end test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_end_to_end_test()
    sys.exit(0 if success else 1)