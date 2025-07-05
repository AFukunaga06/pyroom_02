"""
Unit tests for repository layer components.
"""
import pytest
from unittest.mock import Mock, patch, mock_open
from src.models.data_models import Config, FileOperationError
from src.repositories.file_repository import FileRepository
from src.repositories.api_client import ApiClient


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


class TestFileRepository:
    def test_read_input_file(self, mock_config):
        with patch('builtins.open', mock_open(read_data="test content")):
            with patch('os.path.exists', return_value=True):
                repo = FileRepository(mock_config)
                content = repo.read_input_file()
                assert content == "test content"
    
    def test_append_to_input(self, mock_config):
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('os.path.exists', return_value=True):
                repo = FileRepository(mock_config)
                repo.append_to_input("test data")
                mock_file.assert_called_with("test_input.txt", 'a', encoding='utf-8')


class TestApiClient:
    def test_validate_jan_code_valid(self, mock_config):
        client = ApiClient(mock_config)
        assert client.validate_jan_code("1234567890123") == True
        assert client.validate_jan_code("12345678") == True
    
    def test_validate_jan_code_invalid(self, mock_config):
        client = ApiClient(mock_config)
        assert client.validate_jan_code("123") == False
        assert client.validate_jan_code("abc") == False
        assert client.validate_jan_code("") == False
