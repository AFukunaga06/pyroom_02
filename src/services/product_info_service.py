"""
Product information extraction service.
"""
import re
from typing import List, Optional
from ..models.data_models import ProductInfo, JANCodeData, AppError
from ..repositories.file_repository import FileRepository
from ..repositories.api_client import ApiClient
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProductInfoService:
    """商品情報抽出サービス"""
    
    def __init__(self, file_repository: FileRepository, api_client: ApiClient):
        self.file_repository = file_repository
        self.api_client = api_client
    
    def extract_product_info(self) -> List[ProductInfo]:
        """input.txtからJANコードを抽出し、商品情報を取得"""
        try:
            logger.info("Starting product information extraction")
            
            input_content = self.file_repository.read_input_file()
            jan_codes = self._extract_jan_codes(input_content)
            
            products = []
            for jan_code in jan_codes:
                if self.api_client.validate_jan_code(jan_code):
                    product_info = self.api_client.query_product_info(jan_code)
                    if product_info:
                        products.append(product_info)
                    else:
                        products.append(self._create_not_found_product(jan_code))
                else:
                    logger.warning(f"Invalid JAN code format: {jan_code}")
            
            self._write_products_to_output(products)
            
            logger.info(f"Extracted information for {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Failed to extract product information: {str(e)}")
            raise AppError(f"商品情報の抽出に失敗しました: {str(e)}")
    
    def _extract_jan_codes(self, content: str) -> List[str]:
        """テキストからJANコードを抽出"""
        jan_codes = re.findall(r'JANコード\t(\d+)', content)
        
        direct_codes = re.findall(r'\b(\d{8}|\d{13})\b', content)
        jan_codes.extend(direct_codes)
        
        return list(set(jan_codes))
    
    def _create_not_found_product(self, jan_code: str) -> ProductInfo:
        """商品が見つからない場合のProductInfoを作成"""
        return ProductInfo(
            jan=jan_code,
            name=f"商品情報が見つかりませんでした。{jan_code}",
            price=0.0,
            brand="不明",
            retrieved_at=datetime.now(),
            is_discontinued=False
        )
    
    def _write_products_to_output(self, products: List[ProductInfo]) -> None:
        """商品情報をoutput.txtに書き込み"""
        output_lines = []
        output_lines.append("JANコード\t商品名\t価格\t取得日時")
        
        for product in products:
            line = f"{product.jan}\t{product.name}\t{product.price}\t{product.retrieved_at.strftime('%Y-%m-%d %H:%M:%S')}"
            output_lines.append(line)
        
        output_content = '\n'.join(output_lines)
        self.file_repository.write_output(output_content)
    
    def process_clipboard_data(self, jan_code: str, clipboard_data: str) -> None:
        """クリップボードデータを処理してinput.txtに追加"""
        try:
            lines = clipboard_data.split('\n')
            output_data = "\n".join(line.strip() for line in lines if line.strip())
            
            if jan_code:
                output_data = f"JANコード\t{jan_code}\n{output_data}"
            
            self.file_repository.append_to_input(output_data)
            logger.info("Clipboard data processed and added to input file")
            
        except Exception as e:
            logger.error(f"Failed to process clipboard data: {str(e)}")
            raise AppError(f"クリップボードデータの処理に失敗しました: {str(e)}")
    
    def add_discontinued_product(self, jan_code: str) -> None:
        """廃番商品をinput.txtに追加"""
        try:
            if not self.api_client.validate_jan_code(jan_code):
                raise AppError("無効なJANコード形式です")
            
            data = f"JANコード\t{jan_code}\nブランド名\t廃番"
            self.file_repository.append_to_input(data)
            
            logger.info(f"Added discontinued product: {jan_code}")
            
        except Exception as e:
            logger.error(f"Failed to add discontinued product: {str(e)}")
            raise AppError(f"廃番商品の追加に失敗しました: {str(e)}")
