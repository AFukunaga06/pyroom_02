"""
Unit tests for service layer components.
"""
import pytest
from unittest.mock import Mock, patch
from src.models.data_models import Config, ProductInfo, CheckReport
from src.services.jan_coord_service import JanCoordService
from src.services.product_info_service import ProductInfoService
from src.services.sheet_check_service import SheetCheckService


@pytest.fixture
def mock_config():
    return Config(
        api_key="test_key",
        input_path="test_input.txt",
        output_path="test_output.txt",
        checkd01_path="test_checkd01.txt",
        checkd02_path="test_checkd02.txt",
        google_credentials_path="test_credentials.json",
        spreadsheet_id="test_spreadsheet_id"
    )


@pytest.fixture
def mock_file_repository():
    return Mock()


@pytest.fixture
def mock_api_client():
    return Mock()


@pytest.fixture
def mock_clipboard_manager():
    return Mock()


class TestJanCoordService:
    def test_capture_coordinates(self, mock_file_repository, mock_clipboard_manager):
        with patch('src.services.jan_coord_service.pyautogui.position') as mock_position:
            mock_position.return_value = Mock(x=100, y=200)
            
            service = JanCoordService(mock_file_repository, mock_clipboard_manager)
            x, y = service.capture_coordinates()
            
            assert x == 100
            assert y == 200
            mock_file_repository.append_to_input.assert_called_once()


class TestProductInfoService:
    def test_extract_product_info(self, mock_file_repository, mock_api_client):
        mock_file_repository.read_input_file.return_value = "JANコード\t1234567890123"
        mock_api_client.validate_jan_code.return_value = True
        mock_api_client.query_product_info.return_value = ProductInfo(
            jan="1234567890123",
            name="テスト商品",
            price=100.0,
            brand="テストブランド",
            retrieved_at=None
        )
        
        service = ProductInfoService(mock_file_repository, mock_api_client)
        products = service.extract_product_info()
        
        assert len(products) == 1
        assert products[0].jan == "1234567890123"
        assert products[0].name == "テスト商品"


class TestSheetCheckService:
    def test_check_duplicates_and_missing(self, mock_file_repository):
        mock_file_repository.read_input_file.return_value = """JANコード\t1234567890123
ブランド名\tテストブランド
JANコード\t1234567890123
ブランド名\tテストブランド2"""
        
        service = SheetCheckService(mock_file_repository)
        report = service.check_duplicates_and_missing()
        
        assert isinstance(report, CheckReport)
        assert "1234567890123" in report.duplicates
        assert report.total_records == 2
