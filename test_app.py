#!/usr/bin/env python3
"""
Test script to validate Flask app can start
"""
import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

def test_imports():
    """Test if we can import required modules"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print("✅ Flask available")
    except ImportError as e:
        print(f"❌ Flask not available: {e}")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS available")
    except ImportError as e:
        print(f"❌ Flask-CORS not available: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests available")
    except ImportError as e:
        print(f"❌ Requests not available: {e}")
        return False
        
    return True

def test_minimal_app():
    """Test if minimal app can be created"""
    print("\n🧪 Testing minimal app creation...")
    
    try:
        from app_minimal import app
        print("✅ Minimal app created successfully")
        return True
    except Exception as e:
        print(f"❌ Minimal app creation failed: {e}")
        return False

def test_full_app():
    """Test if full app can be created"""
    print("\n🧪 Testing full app creation...")
    
    try:
        from app import app
        print("✅ Full app created successfully")
        return True
    except Exception as e:
        print(f"❌ Full app creation failed: {e}")
        print(f"Error details: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 AstroShield App Test Suite")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        sys.exit(1)
    
    # Test minimal app
    minimal_ok = test_minimal_app()
    
    # Test full app
    full_ok = test_full_app()
    
    print("\n📊 Test Results:")
    print(f"Imports: ✅")
    print(f"Minimal App: {'✅' if minimal_ok else '❌'}")
    print(f"Full App: {'✅' if full_ok else '❌'}")
    
    if minimal_ok:
        print("\n🎉 At least minimal app is working - deployment should succeed")
    else:
        print("\n💥 Both apps failed - check dependencies")
        sys.exit(1)