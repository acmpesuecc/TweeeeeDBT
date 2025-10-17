#!/usr/bin/env python3
"""
TweeeeeDBT Project Structure Validator
Validates that all files are in their correct locations with proper paths.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description=""):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_directory_structure():
    """Validate the complete directory structure"""
    print("🏗️  Checking Project Structure...")
    print("=" * 50)
    
    base_path = Path(__file__).parent.parent
    os.chdir(base_path)
    
    all_good = True
    
    # Root level files
    root_files = [
        ("README.md", "Main README"),
        ("docker-compose.yaml", "Docker compose"),
        (".env", "Environment variables"),
        ("LICENSE", "License file"),
        (".gitignore", "Git ignore")
    ]
    
    for file, desc in root_files:
        if not check_file_exists(file, desc):
            all_good = False
    
    # Source directories and files
    src_structure = {
        "src/": "Source directory",
        "src/__init__.py": "Source package init",
        "src/producers/": "Producers directory", 
        "src/producers/__init__.py": "Producers package init",
        "src/producers/producer.py": "Main producer",
        "src/consumers/": "Consumers directory",
        "src/consumers/__init__.py": "Consumers package init",
        "src/consumers/consumer_geolocation.py": "Geolocation consumer",
        "src/consumers/consumer_teammentions.py": "Team mentions consumer",
        "src/consumers/consumer_userverify.py": "User verify consumer", 
        "src/consumers/consumer_verifieduserwindowed.py": "Windowed consumer",
        "src/stream_processing/": "Stream processing directory",
        "src/stream_processing/__init__.py": "Stream processing package init",
        "src/stream_processing/stream_processing.py": "Main stream processing",
        "src/batch_processing/": "Batch processing directory",
        "src/batch_processing/__init__.py": "Batch processing package init",
        "src/batch_processing/batch_processing.py": "Main batch processing",
        "src/dashboard/": "Dashboard directory",
        "src/dashboard/__init__.py": "Dashboard package init",
        "src/dashboard/dashboard.py": "Streamlit dashboard",
        "src/dashboard/generate_sample_data.py": "Sample data generator",
        "src/dashboard/.streamlit/": "Streamlit config directory"
    }
    
    for path, desc in src_structure.items():
        if not check_file_exists(path, desc):
            all_good = False
    
    # Data directory
    data_files = [
        ("data/", "Data directory"),
        ("data/IPL_2022_tweets.csv", "Main dataset")
    ]
    
    for file, desc in data_files:
        if not check_file_exists(file, desc):
            all_good = False
    
    # Database directory
    db_files = [
        ("db/", "Database directory"),
        ("db/schema.sql", "Database schema"),
        ("db/dbcheck.py", "Database checker")
    ]
    
    for file, desc in db_files:
        if not check_file_exists(file, desc):
            all_good = False
    
    # Documentation directory
    docs_files = [
        ("docs/", "Documentation directory"),
        ("docs/CONTRIBUTING.md", "Contributing guide"),
        ("docs/ProjectReport.pdf", "Project report"),
        ("docs/image.png", "Architecture diagram"),
        ("docs/REORGANIZATION_SUMMARY.md", "Reorganization summary"),
        ("docs/dashboard_README.md", "Dashboard documentation"),
        ("docs/Requirement Specification/", "Requirements directory"),
        ("docs/Requirement Specification/requirements.txt", "Python requirements")
    ]
    
    for file, desc in docs_files:
        if not check_file_exists(file, desc):
            all_good = False
    
    # Scripts directory
    script_files = [
        ("scripts/", "Scripts directory"),
        ("scripts/reset-kafka.sh", "Kafka reset script"),
        ("scripts/run_pipeline.sh", "Pipeline runner script")
    ]
    
    for file, desc in script_files:
        if not check_file_exists(file, desc):
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All files are in their correct locations!")
        print("✅ Project structure validation PASSED")
    else:
        print("❌ Some files are missing or misplaced!")
        print("❌ Project structure validation FAILED")
        return False
    
    return True

def validate_file_contents():
    """Validate that files have correct path references"""
    print("\n🔍 Validating File Contents...")
    print("=" * 50)
    
    all_good = True
    
    # Check producer.py for correct CSV path
    try:
        with open('src/producers/producer.py', 'r') as f:
            content = f.read()
            if '../../data/IPL_2022_tweets.csv' in content:
                print("✅ Producer has correct CSV path")
            else:
                print("❌ Producer has incorrect CSV path")
                all_good = False
    except FileNotFoundError:
        print("❌ Producer file not found")
        all_good = False
    
    # Check dashboard.py for correct .env path
    try:
        with open('src/dashboard/dashboard.py', 'r') as f:
            content = f.read()
            if "load_dotenv(dotenv_path='../../.env')" in content:
                print("✅ Dashboard has correct .env path")
            else:
                print("❌ Dashboard has incorrect .env path")
                all_good = False
    except FileNotFoundError:
        print("❌ Dashboard file not found")  
        all_good = False
    
    # Check batch processing for correct paths
    try:
        with open('src/batch_processing/batch_processing.py', 'r') as f:
            content = f.read()
            if "load_dotenv(dotenv_path='../../.env')" in content and '../../data/IPL_2022_tweets.csv' in content:
                print("✅ Batch processing has correct paths")
            else:
                print("❌ Batch processing has incorrect paths")
                all_good = False
    except FileNotFoundError:
        print("❌ Batch processing file not found")
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("✅ All file contents validated successfully!")
    else:
        print("❌ Some files have incorrect path references!")
        
    return all_good

def main():
    """Main validation function"""
    print("🚀 TweeeeeDBT Project Structure Validator")
    print("🔍 Validating reorganized project structure...\n")
    
    structure_ok = check_directory_structure()
    contents_ok = validate_file_contents()
    
    print("\n" + "=" * 60)
    if structure_ok and contents_ok:
        print("🎉 PROJECT VALIDATION PASSED!")
        print("✅ The project has been successfully reorganized!")
        print("\n📚 Next Steps:")
        print("   1. Run: chmod +x scripts/run_pipeline.sh")
        print("   2. Run: ./scripts/run_pipeline.sh")
        print("   3. Choose option 7 for complete pipeline")
        return 0
    else:
        print("❌ PROJECT VALIDATION FAILED!")
        print("🔧 Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())