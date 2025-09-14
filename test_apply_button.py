#!/usr/bin/env python3
"""
Test script to verify the apply button functionality
"""

import requests
import json
from datetime import datetime

def test_apply_button():
    base_url = "http://localhost:5000"
    
    print("Testing Apply Button Functionality...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return
    
    # Test 2: Check internships API
    try:
        response = requests.get(f"{base_url}/api/internships")
        if response.status_code == 200:
            internships = response.json()
            print(f"✅ Found {len(internships)} internships")
            
            # Test 3: Check individual internship detail pages
            for i, internship in enumerate(internships[:3]):  # Test first 3 internships
                internship_id = internship['id']
                print(f"\nTesting Internship {internship_id}: {internship['title']}")
                
                try:
                    response = requests.get(f"{base_url}/internship/{internship_id}")
                    if response.status_code == 200:
                        print(f"  ✅ Internship detail page loads successfully")
                        
                        # Check if apply button is present in the HTML
                        if 'Apply Now' in response.text:
                            print(f"  ✅ Apply button found in HTML")
                        else:
                            print(f"  ❌ Apply button NOT found in HTML")
                            
                        # Check if application deadline logic is working
                        if 'Application Closed' in response.text:
                            print(f"  ℹ️  Application deadline has passed")
                        elif 'Apply for this Internship' in response.text:
                            print(f"  ℹ️  Application is open")
                        else:
                            print(f"  ⚠️  Application status unclear")
                            
                    else:
                        print(f"  ❌ Failed to load internship detail page (Status: {response.status_code})")
                        
                except Exception as e:
                    print(f"  ❌ Error testing internship {internship_id}: {str(e)}")
                    
        else:
            print("❌ Failed to get internships data")
            
    except Exception as e:
        print(f"❌ Error testing internships API: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_apply_button()
