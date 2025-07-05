"""
Google Sheets repository for handling Google Sheets API operations.
"""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any, Optional
from ..models.data_models import APIError
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsRepository:
    """Google Sheets APIを抽象化するリポジトリクラス"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.worksheet = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Google Sheets APIクライアントを初期化"""
        try:
            creds = Credentials.from_service_account_file(
                self.config.google_credentials_path,
                scopes=[
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
            )
            self.client = gspread.authorize(creds)
            self.worksheet = self.client.open_by_key(self.config.spreadsheet_id).sheet1
            logger.info("Google Sheets client initialized successfully")
        except Exception as e:
            raise APIError(f"Failed to initialize Google Sheets client: {str(e)}")
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """シートからすべてのレコードを取得"""
        try:
            if not self.worksheet:
                self._initialize_client()
            if self.worksheet:
                return self.worksheet.get_all_records()
            else:
                raise APIError("Failed to initialize worksheet")
        except Exception as e:
            raise APIError(f"Failed to get records from Google Sheets: {str(e)}")
    
    def get_jan_codes(self) -> List[str]:
        """シートからJANコードのリストを取得"""
        try:
            records = self.get_all_records()
            jan_codes = []
            for record in records:
                if 'JANコード' in record and record['JANコード']:
                    jan_codes.append(str(record['JANコード']))
            return jan_codes
        except Exception as e:
            raise APIError(f"Failed to get JAN codes from Google Sheets: {str(e)}")
    
    def get_jan_code_by_index(self, index: int) -> Optional[str]:
        """指定されたインデックスのJANコードを取得"""
        try:
            jan_codes = self.get_jan_codes()
            if 0 <= index < len(jan_codes):
                return jan_codes[index]
            return None
        except Exception as e:
            raise APIError(f"Failed to get JAN code by index: {str(e)}")
    
    def update_cell(self, row: int, col: int, value: str) -> None:
        """指定されたセルを更新"""
        try:
            if not self.worksheet:
                self._initialize_client()
            if self.worksheet:
                self.worksheet.update_cell(row, col, value)
                logger.info(f"Updated cell ({row}, {col}) with value: {value}")
            else:
                raise APIError("Failed to initialize worksheet")
        except Exception as e:
            raise APIError(f"Failed to update cell: {str(e)}")
    
    def append_row(self, values: List[str]) -> None:
        """新しい行を追加"""
        try:
            if not self.worksheet:
                self._initialize_client()
            if self.worksheet:
                self.worksheet.append_row(values)
                logger.info(f"Appended row with values: {values}")
            else:
                raise APIError("Failed to initialize worksheet")
        except Exception as e:
            raise APIError(f"Failed to append row: {str(e)}")
