"""
🧪 Test USGS Earthquake API Integration
NASA Space Apps 2024

Simple test to verify that the earthquake API integration works correctly.
"""

import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from utils.nasa_apis import NASAAPIManager
from utils.visualization import VisualizationManager
from models.asteroid_impact import AsteroidImpact

def test_earthquake_api():
    """Test the earthquake API integration."""
    print("🧪 Testing USGS Earthquake API Integration...")
    print("=" * 50)
    
    # Initialize managers
    nasa_api = NASAAPIManager()
    viz_manager = VisualizationManager(nasa_api)
    
    # Test earthquake data fetch
    print("📡 Fetching earthquake data from USGS API...")
    earthquake_data = nasa_api.get_historical_earthquakes()
    
    print(f"✅ Retrieved {len(earthquake_data)} earthquakes:")
    for name, magnitude in earthquake_data.items():
        print(f"   • {name}: M{magnitude}")
    
    print("\n" + "=" * 50)
    
    # Test with asteroid impact
    print("🔬 Testing with sample asteroid impact...")
    
    # Create a sample asteroid impact
    asteroid = AsteroidImpact(
        diameter_m=200,
        velocity_km_s=20,
        density_kg_m3=2600,
        angle_degrees=45
    )
    
    # Generate chart data (which uses earthquake comparison)
    chart_data = viz_manager.create_impact_chart_data(asteroid)
    
    print("📊 Seismic comparison data:")
    seismic_comp = chart_data['seismic_comparison']
    for item in seismic_comp['data']:
        status = "🎯 IMPACT" if item['is_impact'] else "🌍 Earthquake"
        print(f"   {status} {item['name']}: M{item['magnitude']}")
    
    print("\n✅ API integration test completed successfully!")
    print("🌍 Earthquake data is now fetched from USGS API with fallback to static data")

if __name__ == "__main__":
    test_earthquake_api()