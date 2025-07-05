"""
Coordinate capture controller operations.
"""
from typing import Tuple, Optional, Callable
from ..models.data_models import AppError
from ..services.jan_coord_service import JanCoordService
from ..utils.coordinate_capture import CoordinateCapture
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class CoordinateController:
    """座標キャプチャ専用コントローラ"""
    
    def __init__(self, jan_coord_service: JanCoordService):
        self.jan_coord_service = jan_coord_service
        self.coordinate_capture = CoordinateCapture()
        self.status_callback: Optional[Callable[[str], None]] = None
    
    def set_status_callback(self, callback: Callable[[str], None]):
        """ステータス更新コールバックを設定"""
        self.status_callback = callback
    
    def _update_status(self, message: str):
        """ステータスを更新"""
        logger.info(f"Coordinate Status: {message}")
        if self.status_callback:
            self.status_callback(message)
    
    def start_coordinate_capture_mode(self) -> bool:
        """座標キャプチャモードを開始"""
        try:
            self.coordinate_capture.start_capture_mode(self._update_status)
            return True
        except Exception as e:
            logger.error(f"Failed to start coordinate capture mode: {str(e)}")
            raise AppError(f"座標キャプチャモードの開始に失敗しました: {str(e)}")
    
    def stop_coordinate_capture_mode(self) -> bool:
        """座標キャプチャモードを終了"""
        try:
            self.coordinate_capture.stop_capture_mode(self._update_status)
            return True
        except Exception as e:
            logger.error(f"Failed to stop coordinate capture mode: {str(e)}")
            raise AppError(f"座標キャプチャモードの終了に失敗しました: {str(e)}")
    
    def capture_current_position(self) -> Tuple[int, int]:
        """現在のマウス位置をキャプチャ"""
        try:
            return self.jan_coord_service.capture_coordinates()
        except Exception as e:
            logger.error(f"Failed to capture current position: {str(e)}")
            raise AppError(f"現在位置のキャプチャに失敗しました: {str(e)}")
    
    def set_start_position(self) -> Tuple[int, int]:
        """開始位置を設定"""
        try:
            pos = self.coordinate_capture.set_start_position()
            self._update_status(f"開始位置を設定しました: {pos}")
            return pos
        except Exception as e:
            logger.error(f"Failed to set start position: {str(e)}")
            raise AppError(f"開始位置の設定に失敗しました: {str(e)}")
    
    def set_end_position(self) -> Tuple[int, int]:
        """終了位置を設定"""
        try:
            pos = self.coordinate_capture.set_end_position()
            self._update_status(f"終了位置を設定しました: {pos}")
            return pos
        except Exception as e:
            logger.error(f"Failed to set end position: {str(e)}")
            raise AppError(f"終了位置の設定に失敗しました: {str(e)}")
    
    def capture_screen_region(self) -> Optional[str]:
        """画面領域をキャプチャ"""
        try:
            region = self.coordinate_capture.get_capture_region()
            if not region:
                raise AppError("キャプチャ領域が設定されていません")
            
            start_pos, end_pos = region
            content = self.jan_coord_service.capture_screen_region(start_pos, end_pos)
            
            self._update_status("画面領域をキャプチャしました")
            return content
            
        except Exception as e:
            logger.error(f"Failed to capture screen region: {str(e)}")
            raise AppError(f"画面領域のキャプチャに失敗しました: {str(e)}")
    
    def get_current_mouse_position(self) -> Tuple[int, int]:
        """現在のマウス位置を取得"""
        try:
            return self.coordinate_capture.get_current_position()
        except Exception as e:
            logger.error(f"Failed to get current mouse position: {str(e)}")
            raise AppError(f"現在のマウス位置の取得に失敗しました: {str(e)}")
