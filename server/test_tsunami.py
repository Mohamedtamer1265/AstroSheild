"""
🧪 Tsunami Risk Assessment Test
NASA Space Apps 2024

Test script to demonstrate the tsunami risk assessment functionality
without requiring the full Flask server to be running.
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

from utils.nasa_apis import NASAAPIManager

def test_tsunami_assessment():
    """Test the tsunami risk assessment functionality."""
    print("🌊 Tsunami Risk Assessment Test")
    print("=" * 50)
    
    # Initialize NASA API manager
    nasa_manager = NASAAPIManager()
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Chicxulub-like Impact (Yucatan Peninsula)',
            'lat': 21.4,
            'lon': -89.5,
            'diameter_m': 10000,
            'description': 'Large asteroid impact in shallow Gulf of Mexico waters'
        },
        {
            'name': 'Tunguska-like Impact (Siberia)',
            'lat': 60.9,
            'lon': 101.9,
            'diameter_m': 60,
            'description': 'Small airburst over land'
        },
        {
            'name': 'Pacific Ocean Impact',
            'lat': 0.0,
            'lon': -140.0,
            'diameter_m': 500,
            'description': 'Medium asteroid in deep Pacific Ocean'
        },
        {
            'name': 'Mediterranean Impact',
            'lat': 35.0,
            'lon': 20.0,
            'diameter_m': 200,
            'description': 'Small asteroid in Mediterranean Sea'
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🎯 Test {i}: {scenario['name']}")
        print(f"📍 Location: ({scenario['lat']}, {scenario['lon']})")
        print(f"📏 Diameter: {scenario['diameter_m']}m")
        print(f"📝 {scenario['description']}")
        print("-" * 30)
        
        try:
            # Perform tsunami risk assessment
            result = nasa_manager.assess_tsunami_risk(
                impact_lat=scenario['lat'],
                impact_lon=scenario['lon'],
                diameter_m=scenario['diameter_m'],
                search_radius_km=1000
            )
            
            # Display results
            print(f"🌊 Tsunami Risk Level: {result['risk_level'].upper()}")
            print(f"🗺️  Impact Type: {result['location']['impact_type']}")
            print(f"📏 Elevation: {result['location']['elevation_m']:.1f}m")
            
            if result.get('warnings'):
                print("\n⚠️  Warnings:")
                for warning in result['warnings'][:3]:  # Show first 3 warnings
                    print(f"   • {warning}")
            
            # Show size factor
            size_info = result['tsunami_assessment']['size_factor']
            print(f"📊 Size Category: {size_info['category']}")
            
            print(f"✅ Assessment completed successfully")
            
        except Exception as e:
            print(f"❌ Error in assessment: {str(e)}")
            print(f"🔍 This might be due to API connectivity issues")
    
    print(f"\n{'='*50}")
    print("🎉 Tsunami risk assessment test completed!")
    print("\nKey Features Demonstrated:")
    print("• Elevation-based water detection (elevation ≤ 0)")
    print("• Asteroid size categorization")
    print("• Risk level calculation")
    print("• Coastal impact analysis")
    print("• Warning generation system")
    print("\nNote: This test uses live elevation data from Open-Elevation API")

if __name__ == '__main__':
    test_tsunami_assessment()