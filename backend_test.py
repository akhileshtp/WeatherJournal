import requests
import json
import time
import os
import unittest
from urllib.parse import urljoin

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"')
            break

# Ensure the URL doesn't have quotes
BACKEND_URL = BACKEND_URL.strip("'\"")
API_URL = urljoin(BACKEND_URL, '/api')

print(f"Testing against backend URL: {API_URL}")

class YouTubeAudioDownloaderTest(unittest.TestCase):
    
    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(urljoin(API_URL, '/'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['message'], 'YouTube Audio Downloader API')
        print("✅ API root endpoint test passed")
    
    def test_basic_youtube_url(self):
        """Test downloading audio from a basic YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        payload = {
            "url": url,
            "format": "mp3",
            "quality": "high"
        }
        
        response = requests.post(urljoin(API_URL, '/download'), json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['file_path'])
        self.assertIsNotNone(data['title'])
        
        # Test downloading the file
        file_id = data['file_path'].replace('/', '__')
        file_response = requests.get(urljoin(API_URL, f'/download-file/{file_id}'))
        self.assertEqual(file_response.status_code, 200)
        
        print(f"✅ Basic YouTube URL test passed - Downloaded: {data['title']}")
        return data
    
    def test_different_formats(self):
        """Test downloading audio in different formats"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Short video for testing
        formats = ["mp3", "wav", "m4a"]
        
        for format in formats:
            payload = {
                "url": url,
                "format": format,
                "quality": "medium"  # Using medium quality to speed up tests
            }
            
            response = requests.post(urljoin(API_URL, '/download'), json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertTrue(data['success'])
            self.assertIsNotNone(data['file_path'])
            self.assertTrue(data['file_path'].endswith(f'.{format}') or format in data['file_path'])
            
            print(f"✅ Format test passed for {format}")
    
    def test_different_qualities(self):
        """Test downloading audio with different quality settings"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        qualities = ["high", "medium", "low"]
        
        for quality in qualities:
            payload = {
                "url": url,
                "format": "mp3",
                "quality": quality
            }
            
            response = requests.post(urljoin(API_URL, '/download'), json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertTrue(data['success'])
            self.assertIsNotNone(data['file_path'])
            
            print(f"✅ Quality test passed for {quality}")
    
    def test_url_validation(self):
        """Test URL validation with invalid URLs"""
        invalid_urls = [
            "https://www.google.com",
            "https://example.com",
            "not-a-url",
            "http://youtubecom/watch?v=dQw4w9WgXcQ"  # Missing dot
        ]
        
        for url in invalid_urls:
            payload = {
                "url": url,
                "format": "mp3",
                "quality": "high"
            }
            
            response = requests.post(urljoin(API_URL, '/download'), json=payload)
            self.assertEqual(response.status_code, 400)
            
            print(f"✅ URL validation test passed for invalid URL: {url}")
    
    def test_error_handling(self):
        """Test error handling with unavailable videos"""
        # Non-existent video ID
        url = "https://www.youtube.com/watch?v=xxxxxxxxxxx"
        payload = {
            "url": url,
            "format": "mp3",
            "quality": "high"
        }
        
        response = requests.post(urljoin(API_URL, '/download'), json=payload)
        self.assertEqual(response.status_code, 400)
        
        print(f"✅ Error handling test passed for unavailable video")
    
    def test_short_youtube_url(self):
        """Test with a shortened YouTube URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        payload = {
            "url": url,
            "format": "mp3",
            "quality": "high"
        }
        
        response = requests.post(urljoin(API_URL, '/download'), json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['file_path'])
        
        print(f"✅ Short YouTube URL test passed")

if __name__ == "__main__":
    # Run the tests
    print("Starting YouTube Audio Downloader API Tests...")
    
    # First, let's check if the API is reachable
    try:
        response = requests.get(urljoin(API_URL, '/'))
        print(f"API root response: {response.status_code}")
        if response.status_code == 200:
            print(f"API response content: {response.json()}")
        else:
            print(f"API response error: {response.text}")
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
    
    # Create a test suite
    suite = unittest.TestSuite()
    suite.addTest(YouTubeAudioDownloaderTest('test_api_root'))
    
    # Run the basic test first to see if it works
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("✅ API root test passed, continuing with other tests...")
        
        # Add the rest of the tests
        suite = unittest.TestSuite()
        suite.addTest(YouTubeAudioDownloaderTest('test_basic_youtube_url'))
        suite.addTest(YouTubeAudioDownloaderTest('test_different_formats'))
        suite.addTest(YouTubeAudioDownloaderTest('test_different_qualities'))
        suite.addTest(YouTubeAudioDownloaderTest('test_url_validation'))
        suite.addTest(YouTubeAudioDownloaderTest('test_error_handling'))
        suite.addTest(YouTubeAudioDownloaderTest('test_short_youtube_url'))
        
        # Run the tests
        result = runner.run(suite)
    
    # Print summary
    print("\n=== TEST SUMMARY ===")
    print(f"Total tests: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Print detailed error information
    if len(result.failures) > 0:
        print("\n=== FAILURES ===")
        for i, (test, traceback) in enumerate(result.failures):
            print(f"\nFailure {i+1}: {test}")
            print(traceback)
    
    if len(result.errors) > 0:
        print("\n=== ERRORS ===")
        for i, (test, traceback) in enumerate(result.errors):
            print(f"\nError {i+1}: {test}")
            print(traceback)
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("✅ All tests passed successfully!")
    else:
        print("❌ Some tests failed. See details above.")
