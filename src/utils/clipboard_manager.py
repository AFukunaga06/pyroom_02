"""
Clipboard operations utility.
"""
import pyperclip
from typing import Optional
from ..models.data_models import AppError
import logging

logger = logging.getLogger(__name__)


class ClipboardManager:
    """クリップボード操作を管理するクラス"""
    
    @staticmethod
    def copy(text: str) -> None:
        """テキストをクリップボードにコピー"""
        try:
            pyperclip.copy(text)
            logger.info(f"Copied to clipboard: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {str(e)}")
            raise AppError(f"クリップボードへのコピーに失敗しました: {str(e)}")
    
    @staticmethod
    def paste() -> Optional[str]:
        """クリップボードからテキストを取得"""
        try:
            content = pyperclip.paste()
            logger.info(f"Pasted from clipboard: {content[:50] if content else 'None'}...")
            return content
        except Exception as e:
            logger.error(f"Failed to paste from clipboard: {str(e)}")
            raise AppError(f"クリップボードからの取得に失敗しました: {str(e)}")
    
    @staticmethod
    def is_empty() -> bool:
        """クリップボードが空かどうかを確認"""
        try:
            content = pyperclip.paste()
            return not content or content.strip() == ""
        except Exception as e:
            logger.error(f"Failed to check clipboard: {str(e)}")
            return True
