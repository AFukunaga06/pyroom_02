"""
Data validation utilities.
"""
import re
from typing import Optional, List
from ..models.data_models import ValidationError


class DataValidator:
    """データ検証ユーティリティ"""
    
    @staticmethod
    def validate_jan_code(jan_code: str) -> bool:
        """JANコードの形式を検証"""
        if not jan_code or not isinstance(jan_code, str):
            return False
        
        jan_code = jan_code.strip()
        
        if not jan_code.isdigit():
            return False
        
        if len(jan_code) not in [8, 13]:
            return False
        
        return True
    
    @staticmethod
    def validate_coordinates(x: int, y: int) -> bool:
        """座標の妥当性を検証"""
        if not isinstance(x, int) or not isinstance(y, int):
            return False
        
        if x < 0 or y < 0:
            return False
        
        if x > 10000 or y > 10000:
            return False
        
        return True
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """ファイルパスの妥当性を検証"""
        if not file_path or not isinstance(file_path, str):
            return False
        
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in file_path:
                return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """入力テキストをサニタイズ"""
        if not text:
            return ""
        
        text = text.strip()
        
        text = re.sub(r'[^\w\s\-_.,()[\]{}]', '', text, flags=re.UNICODE)
        
        return text
    
    @staticmethod
    def validate_product_data(jan_code: str, name: str, price: float) -> List[str]:
        """商品データの検証"""
        errors = []
        
        if not DataValidator.validate_jan_code(jan_code):
            errors.append("無効なJANコード形式です")
        
        if not name or len(name.strip()) == 0:
            errors.append("商品名が空です")
        
        if price < 0:
            errors.append("価格は0以上である必要があります")
        
        return errors


def validate_jan_code(jan_code: str) -> bool:
    """JANコードの形式を検証（便利関数）"""
    return DataValidator.validate_jan_code(jan_code)


def validate_coordinates(x: int, y: int) -> bool:
    """座標の妥当性を検証（便利関数）"""
    return DataValidator.validate_coordinates(x, y)


def sanitize_input(text: str) -> str:
    """入力テキストをサニタイズ（便利関数）"""
    return DataValidator.sanitize_input(text)
