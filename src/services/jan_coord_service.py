"""
JAN coordinate capture service.
"""
import pyautogui
import time
from typing import Tuple, Optional
from ..models.data_models import InputRecord, AppError
from ..repositories.file_repository import FileRepository
from ..utils.clipboard_manager import ClipboardManager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JanCoordService:
    """JANコード座標取得サービス"""
    
    def __init__(self, file_repository: FileRepository, clipboard_manager: ClipboardManager):
        self.file_repository = file_repository
        self.clipboard_manager = clipboard_manager
    
    def capture_coordinates(self) -> Tuple[int, int]:
        """マウス位置を取得し、座標をファイルに記録"""
        try:
            logger.info("Starting coordinate capture")
            
            pos = pyautogui.position()
            x, y = int(pos.x), int(pos.y)
            timestamp = datetime.now()
            
            record = InputRecord(
                timestamp=timestamp,
                x=x,
                y=y
            )
            
            coord_data = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},{x},{y}"
            self.file_repository.append_to_input(coord_data)
            
            logger.info(f"Captured coordinates: ({x}, {y})")
            return x, y
            
        except Exception as e:
            logger.error(f"Failed to capture coordinates: {str(e)}")
            raise AppError(f"座標取得に失敗しました: {str(e)}")
    
    def copy_last_coordinate_to_clipboard(self) -> str:
        """最後に取得した座標をクリップボードに転送"""
        try:
            input_content = self.file_repository.read_input_file()
            lines = input_content.strip().split('\n')
            
            if not lines or not lines[-1]:
                raise AppError("座標データが見つかりません")
            
            last_line = lines[-1]
            self.clipboard_manager.copy(last_line)
            
            logger.info(f"Copied to clipboard: {last_line}")
            return last_line
            
        except Exception as e:
            logger.error(f"Failed to copy coordinates to clipboard: {str(e)}")
            raise AppError(f"クリップボードへのコピーに失敗しました: {str(e)}")
    
    def capture_screen_region(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> str:
        """指定された範囲のテキストを取得"""
        try:
            x1, y1 = start_pos
            x2, y2 = end_pos
            
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            left = min(x1, x2)
            top = min(y1, y2)
            
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            content = f"画面領域をキャプチャしました: ({left}, {top}, {width}, {height})"
            
            self.file_repository.save_coordinates_and_content(start_pos, end_pos, content)
            
            logger.info(f"Captured screen region: {start_pos} to {end_pos}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to capture screen region: {str(e)}")
            raise AppError(f"画面領域のキャプチャに失敗しました: {str(e)}")
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """現在のマウス位置を取得"""
        try:
            pos = pyautogui.position()
            return int(pos.x), int(pos.y)
        except Exception as e:
            logger.error(f"Failed to get mouse position: {str(e)}")
            raise AppError(f"マウス位置の取得に失敗しました: {str(e)}")
