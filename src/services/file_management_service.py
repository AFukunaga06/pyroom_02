"""
File management service for batch operations.
"""
import subprocess
import os
from typing import List, Optional
from ..models.data_models import AppError
from ..repositories.file_repository import FileRepository
import logging

logger = logging.getLogger(__name__)


class FileManagementService:
    """ファイル管理サービス"""
    
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
    
    def execute_batch_file(self, batch_file_path: str) -> bool:
        """バッチファイルを実行"""
        try:
            if not os.path.exists(batch_file_path):
                raise AppError(f"バッチファイルが見つかりません: {batch_file_path}")
            
            logger.info(f"Executing batch file: {batch_file_path}")
            
            result = subprocess.run(
                [batch_file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Batch file executed successfully: {batch_file_path}")
                return True
            else:
                logger.error(f"Batch file execution failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Batch file execution timed out: {batch_file_path}")
            return False
        except Exception as e:
            logger.error(f"Failed to execute batch file: {str(e)}")
            raise AppError(f"バッチファイルの実行に失敗しました: {str(e)}")
    
    def open_file(self, file_path: str) -> bool:
        """ファイルを開く"""
        try:
            if not os.path.exists(file_path):
                raise AppError(f"ファイルが存在しません: {file_path}")
            
            if os.name == 'nt':
                import subprocess
                subprocess.run(['notepad.exe', file_path], check=False)
            else:
                subprocess.run(['xdg-open', file_path])
            
            logger.info(f"Opened file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open file: {str(e)}")
            raise AppError(f"ファイルを開けませんでした: {str(e)}")
    
    def execute_batch_and_open_file(self, batch_file: str, output_file: str) -> bool:
        """バッチファイルを実行してから出力ファイルを開く"""
        try:
            if self.execute_batch_file(batch_file):
                return self.open_file(output_file)
            return False
            
        except Exception as e:
            logger.error(f"Failed to execute batch and open file: {str(e)}")
            raise AppError(f"バッチ実行とファイル表示に失敗しました: {str(e)}")
    
    def clear_all_files(self) -> None:
        """すべてのファイルをクリア"""
        try:
            self.file_repository.clear_files(['input', 'output', 'checkd01', 'checkd02'])
            logger.info("All files cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear files: {str(e)}")
            raise AppError(f"ファイルのクリアに失敗しました: {str(e)}")
    
    def backup_files(self, backup_dir: str) -> None:
        """ファイルをバックアップ"""
        try:
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            files_to_backup = [
                'input.txt',
                'output.txt',
                'checkd01.txt',
                'checkd02.txt'
            ]
            
            for file_name in files_to_backup:
                if os.path.exists(file_name):
                    backup_path = os.path.join(backup_dir, file_name)
                    subprocess.run(['cp', file_name, backup_path])
            
            logger.info(f"Files backed up to: {backup_dir}")
            
        except Exception as e:
            logger.error(f"Failed to backup files: {str(e)}")
            raise AppError(f"ファイルのバックアップに失敗しました: {str(e)}")
