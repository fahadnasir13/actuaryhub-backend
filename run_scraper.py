#!/usr/bin/env python3
"""
Standalone script to run the job scraper
Usage: python run_scraper.py
"""

import sys
import os
import time
from scraper import JobScraper

def main():
    print("🎯 ActuaryJobs Web Scraper")
    print("=" * 50)
    
    # Check if Flask API is running
    scraper = JobScraper()
    health = scraper.jobService.checkHealth()
    
    if health.get('status') != 'healthy':
        print("⚠️  Warning: Flask API is not running!")
        print("   Please start the Flask server first:")
        print("   cd backend && python app.py")
        print("\n   Continuing with scraping (will use fallback data)...")
        time.sleep(2)
    else:
        print("✅ Flask API is healthy and running")
    
    # Run the scraper
    try:
        jobs = scraper.run_scraper()
        
        if jobs:
            print(f"\n🎉 Successfully scraped {len(jobs)} jobs!")
            print("\n📋 Jobs found:")
            for i, job in enumerate(jobs, 1):
                print(f"   {i}. {job['title']} at {job['company']} ({job['location']})")
        else:
            print("\n❌ No jobs were scraped")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Scraping failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()