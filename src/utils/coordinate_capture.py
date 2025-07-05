"""
Coordinate capture utility.
"""
import pyautogui
import time
from typing import Tuple, Callable, Optional
from ..models.data_models import AppError
import logging

logger = logging.getLogger(__name__)


class CoordinateCapture:
    """座標キャプチャユーティリティ"""
    
    def __init__(self):
        self.is_capturing = False
        self.start_pos = None
        self.end_pos = None
    
    def start_capture_mode(self, callback: Optional[Callable] = None) -> None:
        """座標キャプチャモードを開始"""
        try:
            self.is_capturing = True
            logger.info("Started coordinate capture mode")
            
            if callback:
                callback("座標キャプチャモードを開始しました。クリックして座標を取得してください。")
                
        except Exception as e:
            logger.error(f"Failed to start capture mode: {str(e)}")
            raise AppError(f"座標キャプチャモードの開始に失敗しました: {str(e)}")
    
    def stop_capture_mode(self, callback: Optional[Callable] = None) -> None:
        """座標キャプチャモードを終了"""
        try:
            self.is_capturing = False
            self.start_pos = None
            self.end_pos = None
            logger.info("Stopped coordinate capture mode")
            
            if callback:
                callback("座標キャプチャモードを終了しました。")
                
        except Exception as e:
            logger.error(f"Failed to stop capture mode: {str(e)}")
            raise AppError(f"座標キャプチャモードの終了に失敗しました: {str(e)}")
    
    def get_current_position(self) -> Tuple[int, int]:
        """現在のマウス位置を取得"""
        try:
            pos = pyautogui.position()
            return int(pos.x), int(pos.y)
        except Exception as e:
            logger.error(f"Failed to get current position: {str(e)}")
            raise AppError(f"現在位置の取得に失敗しました: {str(e)}")
    
    def set_start_position(self, pos: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        """開始位置を設定"""
        try:
            if pos is None:
                pos = self.get_current_position()
            
            self.start_pos = pos
            logger.info(f"Set start position: {pos}")
            return pos
            
        except Exception as e:
            logger.error(f"Failed to set start position: {str(e)}")
            raise AppError(f"開始位置の設定に失敗しました: {str(e)}")
    
    def set_end_position(self, pos: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        """終了位置を設定"""
        try:
            if pos is None:
                pos = self.get_current_position()
            
            self.end_pos = pos
            logger.info(f"Set end position: {pos}")
            return pos
            
        except Exception as e:
            logger.error(f"Failed to set end position: {str(e)}")
            raise AppError(f"終了位置の設定に失敗しました: {str(e)}")
    
    def get_capture_region(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """キャプチャ領域を取得"""
        if self.start_pos and self.end_pos:
            return self.start_pos, self.end_pos
        return None
    
    def wait_for_click(self, timeout: int = 30) -> Tuple[int, int]:
        """クリックを待機"""
        try:
            logger.info(f"Waiting for click (timeout: {timeout}s)")
            
            start_time = time.time()
            initial_pos = pyautogui.position()
            
            while time.time() - start_time < timeout:
                pos = pyautogui.position()
                current_pos = (int(pos.x), int(pos.y))
                
                if pyautogui.mouseDown():
                    logger.info(f"Click detected at: {current_pos}")
                    return current_pos
                
                time.sleep(0.1)
            
            raise AppError("クリック待機がタイムアウトしました")
            
        except Exception as e:
            logger.error(f"Failed to wait for click: {str(e)}")
            raise AppError(f"クリック待機に失敗しました: {str(e)}")
