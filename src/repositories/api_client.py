"""
API client for external product information services.
"""
import requests
from typing import Dict, Any, Optional
from ..models.data_models import ProductInfo, APIError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ApiClient:
    """外部API呼び出しを抽象化するクライアントクラス"""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JANCode-Management-System/1.0'
        })
    
    def query_product_info(self, jan_code: str) -> Optional[ProductInfo]:
        """JANコードから商品情報を取得"""
        try:
            response = self._make_request(jan_code)
            if response and response.get('success'):
                return self._parse_product_info(jan_code, response)
            else:
                logger.warning(f"Product not found for JAN code: {jan_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to query product info for {jan_code}: {str(e)}")
            return None
    
    def _make_request(self, jan_code: str) -> Optional[Dict[str, Any]]:
        """API リクエストを実行（リトライ機能付き）"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = f"https://api.example.com/product/{jan_code}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return {'success': False, 'error': 'Product not found'}
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise APIError(f"API request failed after {max_retries} attempts: {str(e)}")
        
        return None
    
    def _parse_product_info(self, jan_code: str, response: Dict[str, Any]) -> ProductInfo:
        """APIレスポンスからProductInfoオブジェクトを作成"""
        data = response.get('data', {})
        return ProductInfo(
            jan=jan_code,
            name=data.get('name', '商品情報が見つかりませんでした。'),
            price=float(data.get('price', 0.0)),
            brand=data.get('brand', '不明'),
            retrieved_at=datetime.now(),
            is_discontinued=data.get('discontinued', False)
        )
    
    def validate_jan_code(self, jan_code: str) -> bool:
        """JANコードの形式を検証"""
        if not jan_code or not jan_code.isdigit():
            return False
        
        if len(jan_code) not in [8, 13]:
            return False
        
        return True
