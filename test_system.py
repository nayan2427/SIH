#!/usr/bin/env python3
"""
System Testing Script for InternshipHub
Tests all major functionality of the internship platform
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"

class InternshipHubTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def test_server_running(self):
        """Test if the server is running"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("Server Running", True, "Server is responding")
                return True
            else:
                self.log_test("Server Running", False, f"Server returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_test("Server Running", False, "Cannot connect to server")
            return False
            
    def test_homepage_loads(self):
        """Test if homepage loads correctly"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200 and "InternshipHub" in response.text:
                self.log_test("Homepage Loads", True, "Homepage content loaded successfully")
                return True
            else:
                self.log_test("Homepage Loads", False, "Homepage content not found")
                return False
        except Exception as e:
            self.log_test("Homepage Loads", False, f"Error: {str(e)}")
            return False
            
    def test_internships_api(self):
        """Test internships API endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/internships")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_test("Internships API", True, f"Found {len(data)} internships")
                    return True
                else:
                    self.log_test("Internships API", False, "No internships data returned")
                    return False
            else:
                self.log_test("Internships API", False, f"API returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Internships API", False, f"Error: {str(e)}")
            return False
            
    def test_stats_api(self):
        """Test statistics API endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/api/stats")
            if response.status_code == 200:
                data = response.json()
                required_keys = ['total_internships', 'trust_internships', 'government_internships', 'private_internships']
                if all(key in data for key in required_keys):
                    self.log_test("Stats API", True, f"Stats: {data['total_internships']} total internships")
                    return True
                else:
                    self.log_test("Stats API", False, "Missing required stats fields")
                    return False
            else:
                self.log_test("Stats API", False, f"API returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Stats API", False, f"Error: {str(e)}")
            return False
            
    def test_internships_page(self):
        """Test internships browsing page"""
        try:
            response = self.session.get(f"{BASE_URL}/internships")
            if response.status_code == 200 and "Browse Internships" in response.text:
                self.log_test("Internships Page", True, "Internships page loaded successfully")
                return True
            else:
                self.log_test("Internships Page", False, "Internships page not loading correctly")
                return False
        except Exception as e:
            self.log_test("Internships Page", False, f"Error: {str(e)}")
            return False
            
    def test_login_page(self):
        """Test login page"""
        try:
            response = self.session.get(f"{BASE_URL}/login")
            if response.status_code == 200 and "Welcome Back" in response.text:
                self.log_test("Login Page", True, "Login page loaded successfully")
                return True
            else:
                self.log_test("Login Page", False, "Login page not loading correctly")
                return False
        except Exception as e:
            self.log_test("Login Page", False, f"Error: {str(e)}")
            return False
            
    def test_register_page(self):
        """Test registration page"""
        try:
            response = self.session.get(f"{BASE_URL}/register")
            if response.status_code == 200 and "Create Your Profile" in response.text:
                self.log_test("Register Page", True, "Registration page loaded successfully")
                return True
            else:
                self.log_test("Register Page", False, "Registration page not loading correctly")
                return False
        except Exception as e:
            self.log_test("Register Page", False, f"Error: {str(e)}")
            return False
            
    def test_user_registration(self):
        """Test user registration functionality"""
        try:
            # Generate unique email for testing
            timestamp = int(time.time())
            test_email = f"test{timestamp}@example.com"
            
            registration_data = {
                'name': 'Test User',
                'email': test_email,
                'mobile': '9876543210',
                'education_level': "Bachelor's",
                'field_of_study': 'Computer Science',
                'university': 'Test University',
                'graduation_year': '2024',
                'skills': 'Python, JavaScript'
            }
            
            response = self.session.post(f"{BASE_URL}/register", data=registration_data)
            if response.status_code == 302:  # Redirect after successful registration
                self.log_test("User Registration", True, "User registered successfully")
                return True
            else:
                self.log_test("User Registration", False, f"Registration failed with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
            
    def test_mobile_responsiveness(self):
        """Test mobile responsiveness by checking viewport meta tag"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if 'viewport' in response.text and 'width=device-width' in response.text:
                self.log_test("Mobile Responsive", True, "Viewport meta tag found")
                return True
            else:
                self.log_test("Mobile Responsive", False, "Viewport meta tag not found")
                return False
        except Exception as e:
            self.log_test("Mobile Responsive", False, f"Error: {str(e)}")
            return False
            
    def test_css_loading(self):
        """Test if CSS files are loading"""
        try:
            response = self.session.get(f"{BASE_URL}/static/styles.css")
            if response.status_code == 200 and 'body' in response.text:
                self.log_test("CSS Loading", True, "CSS file loaded successfully")
                return True
            else:
                self.log_test("CSS Loading", False, "CSS file not loading correctly")
                return False
        except Exception as e:
            self.log_test("CSS Loading", False, f"Error: {str(e)}")
            return False
            
    def test_js_loading(self):
        """Test if JavaScript files are loading"""
        try:
            response = self.session.get(f"{BASE_URL}/static/script.js")
            if response.status_code == 200 and 'function' in response.text:
                self.log_test("JavaScript Loading", True, "JavaScript file loaded successfully")
                return True
            else:
                self.log_test("JavaScript Loading", False, "JavaScript file not loading correctly")
                return False
        except Exception as e:
            self.log_test("JavaScript Loading", False, f"Error: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("INTERNSHIPHUB SYSTEM TESTING")
        print("=" * 60)
        print(f"Testing server at: {BASE_URL}")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Core functionality tests
        self.test_server_running()
        self.test_homepage_loads()
        self.test_internships_api()
        self.test_stats_api()
        self.test_internships_page()
        
        # User interface tests
        self.test_login_page()
        self.test_register_page()
        self.test_user_registration()
        
        # Technical tests
        self.test_mobile_responsiveness()
        self.test_css_loading()
        self.test_js_loading()
        
        # Generate test report
        self.generate_report()
        
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save detailed report
        report_data = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100,
                "test_date": datetime.now().isoformat()
            },
            "test_results": self.test_results
        }
        
        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nDetailed report saved to: test_report.json")
        print("=" * 60)

if __name__ == "__main__":
    tester = InternshipHubTester()
    tester.run_all_tests()
