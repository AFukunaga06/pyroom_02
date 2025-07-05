"""
JAN code specific controller operations.
"""
from typing import List, Optional
from ..models.data_models import JANCodeData, AppError
from ..services.product_info_service import ProductInfoService
from ..services.sheet_check_service import SheetCheckService
from ..repositories.google_sheets_repository import GoogleSheetsRepository
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class JanCodeController:
    """JANコード専用コントローラ"""
    
    def __init__(self, product_service: ProductInfoService, 
                 sheet_service: SheetCheckService,
                 sheets_repository: GoogleSheetsRepository):
        self.product_service = product_service
        self.sheet_service = sheet_service
        self.sheets_repository = sheets_repository
    
    def get_jan_codes_from_sheets(self) -> List[str]:
        """Google SheetsからJANコードのリストを取得"""
        try:
            return self.sheets_repository.get_jan_codes()
        except Exception as e:
            logger.error(f"Failed to get JAN codes from sheets: {str(e)}")
            raise AppError(f"Google SheetsからJANコードの取得に失敗しました: {str(e)}")
    
    def get_jan_code_by_index(self, index: int) -> Optional[str]:
        """指定されたインデックスのJANコードを取得"""
        try:
            return self.sheets_repository.get_jan_code_by_index(index)
        except Exception as e:
            logger.error(f"Failed to get JAN code by index: {str(e)}")
            raise AppError(f"JANコードの取得に失敗しました: {str(e)}")
    
    def get_current_jan_code_info(self) -> tuple[int, str]:
        """現在のJANコード情報を取得"""
        try:
            return self.sheet_service.get_jan_code_count_and_current()
        except Exception as e:
            logger.error(f"Failed to get current JAN code info: {str(e)}")
            return 0, ""
    
    def validate_and_add_jan_code(self, jan_code: str, is_discontinued: bool = False) -> bool:
        """JANコードを検証して追加"""
        try:
            if is_discontinued:
                self.product_service.add_discontinued_product(jan_code)
            else:
                clipboard_data = f"JANコード\t{jan_code}"
                self.product_service.process_clipboard_data(jan_code, clipboard_data)
            
            return True
            
        except AppError as e:
            logger.error(f"Failed to add JAN code: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error adding JAN code: {str(e)}")
            raise AppError(f"JANコードの追加中に予期しないエラーが発生しました: {str(e)}")
