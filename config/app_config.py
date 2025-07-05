"""
Application configuration management.
"""
import os
import json
from typing import Dict, Any
from src.models.data_models import Config, AppError


class AppConfig:
    """アプリケーション設定管理クラス"""
    
    DEFAULT_CONFIG = {
        'input_path': 'input.txt',
        'output_path': 'output.txt',
        'checkd01_path': 'checkd01.txt',
        'checkd02_path': 'checkd02.txt',
        'google_credentials_path': 'samplep20240906-5ae36c9a4acd.json',
        'spreadsheet_id': '17Le1KA9nzMREt0Qp9_elM1OF1q8aSp-GDBZRPOntNI8',
        'api_key': '',
        'log_level': 'INFO',
        'max_retries': 3,
        'timeout': 30
    }
    
    @classmethod
    def load_config(cls, config_file: str = 'config/config.json') -> Config:
        """設定ファイルから設定を読み込み"""
        try:
            config_data = cls.DEFAULT_CONFIG.copy()
            
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                config_data.update(file_config)
            
            return Config(
                api_key=config_data['api_key'],
                input_path=config_data['input_path'],
                output_path=config_data['output_path'],
                checkd01_path=config_data['checkd01_path'],
                checkd02_path=config_data['checkd02_path'],
                google_credentials_path=config_data['google_credentials_path'],
                spreadsheet_id=config_data['spreadsheet_id']
            )
            
        except Exception as e:
            raise AppError(f"設定の読み込みに失敗しました: {str(e)}")
    
    @classmethod
    def save_config(cls, config: Config, config_file: str = 'config/config.json') -> None:
        """設定をファイルに保存"""
        try:
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            
            config_data = {
                'api_key': config.api_key,
                'input_path': config.input_path,
                'output_path': config.output_path,
                'checkd01_path': config.checkd01_path,
                'checkd02_path': config.checkd02_path,
                'google_credentials_path': config.google_credentials_path,
                'spreadsheet_id': config.spreadsheet_id
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise AppError(f"設定の保存に失敗しました: {str(e)}")
    
    @classmethod
    def get_default_config(cls) -> Config:
        """デフォルト設定を取得"""
        return Config(
            api_key=cls.DEFAULT_CONFIG['api_key'],
            input_path=cls.DEFAULT_CONFIG['input_path'],
            output_path=cls.DEFAULT_CONFIG['output_path'],
            checkd01_path=cls.DEFAULT_CONFIG['checkd01_path'],
            checkd02_path=cls.DEFAULT_CONFIG['checkd02_path'],
            google_credentials_path=cls.DEFAULT_CONFIG['google_credentials_path'],
            spreadsheet_id=cls.DEFAULT_CONFIG['spreadsheet_id']
        )


def load_config(config_file: str = 'config/config.json') -> Config:
    """設定ファイルから設定を読み込み（便利関数）"""
    return AppConfig.load_config(config_file)
