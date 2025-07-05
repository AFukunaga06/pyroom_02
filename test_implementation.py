#!/usr/bin/env python3
"""
Test script to verify the JANコード management system implementation.
"""

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing module imports...")
    
    try:
        from src.models.data_models import Config, InputRecord, ProductInfo, CheckReport
        print("✅ Data models imported successfully")
    except ImportError as e:
        print(f"❌ Data models import failed: {e}")
        return False
    
    try:
        from src.repositories.file_repository import FileRepository
        from src.repositories.api_client import ApiClient
        from src.repositories.google_sheets_repository import GoogleSheetsRepository
        print("✅ Repository layer imported successfully")
    except ImportError as e:
        print(f"❌ Repository layer import failed: {e}")
        return False
    
    try:
        from src.services.jan_coord_service import JanCoordService
        from src.services.product_info_service import ProductInfoService
        from src.services.sheet_check_service import SheetCheckService
        from src.services.file_management_service import FileManagementService
        print("✅ Service layer imported successfully")
    except ImportError as e:
        print(f"❌ Service layer import failed: {e}")
        return False
    
    try:
        from src.controllers.main_controller import MainController
        from src.controllers.jan_code_controller import JanCodeController
        from src.controllers.coordinate_controller import CoordinateController
        print("✅ Controller layer imported successfully")
    except ImportError as e:
        print(f"❌ Controller layer import failed: {e}")
        return False
    
    try:
        from src.utils.clipboard_manager import ClipboardManager
        from src.utils.coordinate_capture import CoordinateCapture
        from src.utils.logger import setup_logger
        from src.utils.validators import validate_jan_code
        print("✅ Utility modules imported successfully")
    except ImportError as e:
        print(f"❌ Utility modules import failed: {e}")
        return False
    
    return True

def test_config_loading():
    """Test configuration loading."""
    print("\nTesting configuration loading...")
    
    try:
        from config.app_config import AppConfig
        config = AppConfig.load_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   - Input path: {config.input_path}")
        print(f"   - Output path: {config.output_path}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_file_operations():
    """Test basic file operations."""
    print("\nTesting file operations...")
    
    try:
        from src.repositories.file_repository import FileRepository
        from config.app_config import AppConfig
        
        config = AppConfig.load_config()
        repo = FileRepository(config)
        
        if repo.file_exists('input'):
            input_data = repo.read_input_data()
            print(f"✅ Input file read successfully ({len(input_data)} records)")
        else:
            print("ℹ️  Input file does not exist (this is normal)")
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_external_dependencies():
    """Test external dependencies."""
    print("\nTesting external dependencies...")
    
    try:
        import customtkinter
        print(f"✅ CustomTkinter version: {customtkinter.__version__}")
    except ImportError:
        print("❌ CustomTkinter not available")
        return False
    
    try:
        import pyautogui
        print("✅ PyAutoGUI available")
    except ImportError:
        print("❌ PyAutoGUI not available")
        return False
    
    try:
        import pyperclip
        print("✅ Pyperclip available")
    except ImportError:
        print("❌ Pyperclip not available")
        return False
    
    try:
        from google.oauth2.service_account import Credentials
        print("✅ Google API client available")
    except ImportError:
        print("❌ Google API client not available")
        return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("JANコード Management System Implementation Test")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_config_loading()
    all_passed &= test_file_operations()
    all_passed &= test_external_dependencies()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Implementation is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    main()
