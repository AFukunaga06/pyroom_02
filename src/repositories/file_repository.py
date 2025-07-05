"""
File repository for handling local file operations.
"""
import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.data_models import InputRecord, JANCodeData, FileOperationError
import logging

logger = logging.getLogger(__name__)


class FileRepository:
    """ファイル読み書きを抽象化するリポジトリクラス"""
    
    def __init__(self, config):
        self.config = config
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """必要なファイルが存在することを確認"""
        files_to_check = [
            self.config.input_path,
            self.config.output_path,
            self.config.checkd01_path,
            self.config.checkd02_path
        ]
        
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        pass
                    logger.info(f"Created file: {file_path}")
                except Exception as e:
                    raise FileOperationError(f"Failed to create file {file_path}: {str(e)}")
    
    def read_input_file(self) -> str:
        """input.txtの内容を読み取り"""
        try:
            with open(self.config.input_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise FileOperationError(f"Failed to read input file: {str(e)}")
    
    def append_to_input(self, data: str) -> None:
        """input.txtにデータを追記"""
        try:
            with open(self.config.input_path, 'a', encoding='utf-8') as f:
                f.write(data + '\n\n')
            logger.info("Data appended to input file")
        except Exception as e:
            raise FileOperationError(f"Failed to append to input file: {str(e)}")
    
    def write_output(self, data: str) -> None:
        """output.txtにデータを書き込み"""
        try:
            with open(self.config.output_path, 'w', encoding='utf-8') as f:
                f.write(data)
            logger.info("Data written to output file")
        except Exception as e:
            raise FileOperationError(f"Failed to write output file: {str(e)}")
    
    def read_checkd_files(self) -> tuple[List[str], List[str]]:
        """checkd01.txtとcheckd02.txtの内容を読み取り"""
        try:
            with open(self.config.checkd01_path, 'r', encoding='utf-8') as f1:
                lines1 = f1.readlines()
            with open(self.config.checkd02_path, 'r', encoding='utf-8') as f2:
                lines2 = f2.readlines()
            return lines1, lines2
        except Exception as e:
            raise FileOperationError(f"Failed to read checkd files: {str(e)}")
    
    def write_checkd_file(self, file_type: str, data: str) -> None:
        """checkdファイルにデータを書き込み"""
        file_path = self.config.checkd01_path if file_type == 'checkd01' else self.config.checkd02_path
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            logger.info(f"Data written to {file_type} file")
        except Exception as e:
            raise FileOperationError(f"Failed to write {file_type} file: {str(e)}")
    
    def clear_files(self, file_types: List[str]) -> None:
        """指定されたファイルをクリア"""
        file_map = {
            'input': self.config.input_path,
            'output': self.config.output_path,
            'checkd01': self.config.checkd01_path,
            'checkd02': self.config.checkd02_path
        }
        
        for file_type in file_types:
            if file_type in file_map:
                try:
                    with open(file_map[file_type], 'w', encoding='utf-8') as f:
                        f.write('')
                    logger.info(f"Cleared {file_type} file")
                except Exception as e:
                    raise FileOperationError(f"Failed to clear {file_type} file: {str(e)}")
    
    def save_coordinates_and_content(self, start_pos: tuple, end_pos: tuple, content: str) -> None:
        """座標とコピーした内容を保存"""
        try:
            with open('coordinates_and_content.txt', 'w', encoding='utf-8') as f:
                f.write(f"開始位置: {start_pos}\n")
                f.write(f"終了位置: {end_pos}\n")
                f.write(f"コピーした内容:\n{content}\n")
            logger.info("Coordinates and content saved")
        except Exception as e:
            raise FileOperationError(f"Failed to save coordinates: {str(e)}")
    
    def file_exists(self, file_type: str) -> bool:
        """指定されたファイルが存在するかチェック"""
        file_map = {
            'input': self.config.input_path,
            'output': self.config.output_path,
            'checkd01': self.config.checkd01_path,
            'checkd02': self.config.checkd02_path
        }
        
        if file_type in file_map:
            return os.path.exists(file_map[file_type])
        return False
    
    def read_input_data(self) -> List[str]:
        """input.txtのデータを行ごとに読み取り"""
        try:
            with open(self.config.input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
        except Exception as e:
            raise FileOperationError(f"Failed to read input data: {str(e)}")
