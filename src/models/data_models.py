"""
Data models for the JANコード management system.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Config:
    """Configuration settings for the application."""
    api_key: str
    input_path: str
    output_path: str
    checkd01_path: str
    checkd02_path: str
    google_credentials_path: str
    spreadsheet_id: str


@dataclass
class InputRecord:
    """座標取得結果を表すデータモデル"""
    timestamp: datetime
    x: int
    y: int
    content: Optional[str] = None


@dataclass
class ProductInfo:
    """API から得た商品情報を表すデータモデル"""
    jan: str
    name: str
    price: float
    brand: str
    retrieved_at: datetime
    is_discontinued: bool = False


@dataclass
class CheckReport:
    """シートチェックの結果を表すデータモデル"""
    duplicates: List[str]
    missing: Dict[str, List[int]]
    discontinued: List[str]
    total_records: int
    check_timestamp: datetime


@dataclass
class JANCodeData:
    """JANコードとその関連データ"""
    jan_code: str
    brand_name: Optional[str] = None
    product_name: Optional[str] = None
    price: Optional[float] = None
    is_discontinued: bool = False
    line_number: Optional[int] = None


class AppError(Exception):
    """アプリケーション固有のエラー"""
    pass


class FileOperationError(AppError):
    """ファイル操作エラー"""
    pass


class APIError(AppError):
    """API呼び出しエラー"""
    pass


class ValidationError(AppError):
    """データ検証エラー"""
    pass
