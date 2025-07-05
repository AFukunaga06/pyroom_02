"""
Main controller for coordinating all application services.
"""
from typing import Optional, Callable
from ..models.data_models import Config, AppError, CheckReport
from ..services.jan_coord_service import JanCoordService
from ..services.product_info_service import ProductInfoService
from ..services.sheet_check_service import SheetCheckService
from ..services.file_management_service import FileManagementService
from ..repositories.file_repository import FileRepository
from ..repositories.google_sheets_repository import GoogleSheetsRepository
from ..repositories.api_client import ApiClient
from ..utils.clipboard_manager import ClipboardManager
from ..utils.logger import setup_logger
import logging

logger = setup_logger(__name__)


class MainController:
    """メインコントローラ - GUI からの要求を受け取り、各サービスを呼び出す"""
    
    def __init__(self, config: Config):
        self.config = config
        self.status_callback: Optional[Callable[[str], None]] = None
        self.error_callback: Optional[Callable[[str], None]] = None
        
        self._initialize_repositories()
        self._initialize_services()
    
    def _initialize_repositories(self):
        """リポジトリを初期化"""
        try:
            self.file_repository = FileRepository(self.config)
            self.google_sheets_repository = GoogleSheetsRepository(self.config)
            self.api_client = ApiClient(self.config)
            logger.info("Repositories initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize repositories: {str(e)}")
            raise AppError(f"リポジトリの初期化に失敗しました: {str(e)}")
    
    def _initialize_services(self):
        """サービスを初期化"""
        try:
            clipboard_manager = ClipboardManager()
            
            self.jan_coord_service = JanCoordService(self.file_repository, clipboard_manager)
            self.product_info_service = ProductInfoService(self.file_repository, self.api_client)
            self.sheet_check_service = SheetCheckService(self.file_repository)
            self.file_management_service = FileManagementService(self.file_repository)
            
            logger.info("Services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize services: {str(e)}")
            raise AppError(f"サービスの初期化に失敗しました: {str(e)}")
    
    def set_status_callback(self, callback: Callable[[str], None]):
        """ステータス更新コールバックを設定"""
        self.status_callback = callback
    
    def set_error_callback(self, callback: Callable[[str], None]):
        """エラー表示コールバックを設定"""
        self.error_callback = callback
    
    def _update_status(self, message: str):
        """ステータスを更新"""
        logger.info(f"Status: {message}")
        if self.status_callback:
            self.status_callback(message)
    
    def _show_error(self, message: str):
        """エラーを表示"""
        logger.error(f"Error: {message}")
        if self.error_callback:
            self.error_callback(message)
    
    def capture_jan_coordinates(self) -> bool:
        """JAN座標取得を実行"""
        try:
            self._update_status("座標取得を開始しています...")
            
            x, y = self.jan_coord_service.capture_coordinates()
            
            self._update_status(f"座標を取得しました: ({x}, {y})")
            return True
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"座標取得中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def copy_jan_code(self) -> bool:
        """JANコードコピーを実行"""
        try:
            self._update_status("JANコードをクリップボードにコピーしています...")
            
            copied_data = self.jan_coord_service.copy_last_coordinate_to_clipboard()
            
            self._update_status(f"クリップボードにコピーしました: {copied_data}")
            return True
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"JANコードコピー中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def extract_product_info(self) -> bool:
        """商品情報抽出を実行"""
        try:
            self._update_status("商品情報を抽出しています...")
            
            products = self.product_info_service.extract_product_info()
            
            self._update_status(f"{len(products)}件の商品情報を抽出しました")
            return True
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"商品情報抽出中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def check_sheet_data(self) -> Optional[CheckReport]:
        """シートチェックを実行"""
        try:
            self._update_status("シートデータをチェックしています...")
            
            report = self.sheet_check_service.check_duplicates_and_missing()
            
            status_msg = f"チェック完了: 重複{len(report.duplicates)}件, 廃番{len(report.discontinued)}件"
            self._update_status(status_msg)
            
            return report
            
        except AppError as e:
            self._show_error(str(e))
            return None
        except Exception as e:
            error_msg = f"シートチェック中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return None
    
    def execute_batch_operation(self) -> bool:
        """一括実行を実行"""
        try:
            self._update_status("一括処理を開始しています...")
            
            success_count = 0
            total_operations = 4
            
            if self.capture_jan_coordinates():
                success_count += 1
            
            if self.copy_jan_code():
                success_count += 1
            
            if self.extract_product_info():
                success_count += 1
            
            if self.check_sheet_data():
                success_count += 1
            
            self._update_status(f"一括処理完了: {success_count}/{total_operations}件成功")
            return success_count == total_operations
            
        except Exception as e:
            error_msg = f"一括処理中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def process_clipboard_data(self, jan_code: str = "") -> bool:
        """クリップボードデータを処理"""
        try:
            self._update_status("クリップボードデータを処理しています...")
            
            clipboard_data = ClipboardManager.paste()
            if not clipboard_data:
                self._show_error("クリップボードにデータがありません")
                return False
            
            self.product_info_service.process_clipboard_data(jan_code, clipboard_data)
            
            self._update_status("クリップボードデータを処理しました")
            return True
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"クリップボードデータ処理中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def add_discontinued_product(self, jan_code: str) -> bool:
        """廃番商品を追加"""
        try:
            self._update_status("廃番商品を追加しています...")
            
            self.product_info_service.add_discontinued_product(jan_code)
            
            self._update_status(f"廃番商品を追加しました: {jan_code}")
            return True
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"廃番商品追加中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def execute_batch_file(self, batch_file: str, output_file: str = "") -> bool:
        """バッチファイルを実行"""
        try:
            self._update_status(f"バッチファイルを実行しています: {batch_file}")
            
            if output_file:
                success = self.file_management_service.execute_batch_and_open_file(batch_file, output_file)
            else:
                success = self.file_management_service.execute_batch_file(batch_file)
            
            if success:
                self._update_status("バッチファイルの実行が完了しました")
            else:
                self._show_error("バッチファイルの実行に失敗しました")
            
            return success
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"バッチファイル実行中に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
    
    def open_file(self, file_path: str) -> bool:
        """ファイルを開く"""
        try:
            self._update_status(f"ファイルを開いています: {file_path}")
            
            success = self.file_management_service.open_file(file_path)
            
            if success:
                self._update_status("ファイルを開きました")
            else:
                self._show_error("ファイルを開けませんでした")
            
            return success
            
        except AppError as e:
            self._show_error(str(e))
            return False
        except Exception as e:
            error_msg = f"ファイルを開く際に予期しないエラーが発生しました: {str(e)}"
            self._show_error(error_msg)
            return False
