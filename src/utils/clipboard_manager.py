"""
Clipboard operations utility.
"""
import os
from typing import Optional
from ..models.data_models import AppError
import logging

logger = logging.getLogger(__name__)

HEADLESS_MODE = os.environ.get('DISPLAY') is None

if not HEADLESS_MODE:
    try:
        import pyperclip
        CLIPBOARD_AVAILABLE = True
    except ImportError:
        CLIPBOARD_AVAILABLE = False
        logger.warning("Pyperclip not available")
else:
    CLIPBOARD_AVAILABLE = False
    logger.info("Running in headless mode - clipboard operations will be mocked")


class ClipboardManager:
    """クリップボード操作を管理するクラス"""
    
    @staticmethod
    def copy(text: str) -> None:
        """テキストをクリップボードにコピー"""
        try:
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(text)
            else:
                logger.info(f"Mock clipboard copy: {text[:50]}...")
            logger.info(f"Copied to clipboard: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {str(e)}")
            raise AppError(f"クリップボードへのコピーに失敗しました: {str(e)}")
    
    @staticmethod
    def paste() -> Optional[str]:
        """クリップボードからテキストを取得"""
        try:
            if CLIPBOARD_AVAILABLE:
                content = pyperclip.paste()
            else:
                content = "Mock clipboard content"
                logger.info("Mock clipboard content retrieved")
            logger.info(f"Pasted from clipboard: {content[:50] if content else 'None'}...")
            return content
        except Exception as e:
            logger.error(f"Failed to paste from clipboard: {str(e)}")
            raise AppError(f"クリップボードからの取得に失敗しました: {str(e)}")
    
    @staticmethod
    def is_empty() -> bool:
        """クリップボードが空かどうかを確認"""
        try:
            if CLIPBOARD_AVAILABLE:
                content = pyperclip.paste()
                return not content or content.strip() == ""
            else:
                return False  # Mock clipboard is never empty
        except Exception as e:
            logger.error(f"Failed to check clipboard: {str(e)}")
            return True
