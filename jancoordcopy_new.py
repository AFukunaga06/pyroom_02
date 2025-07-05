import customtkinter as ctk
from tkinter import messagebox
import pyperclip
import threading
import time
import pyautogui
import os
from src.models.data_models import Config, AppError
from src.controllers.jan_code_controller import JanCodeController
from src.controllers.coordinate_controller import CoordinateController
from src.repositories.google_sheets_repository import GoogleSheetsRepository
from src.repositories.file_repository import FileRepository
from src.repositories.api_client import ApiClient
from src.services.product_info_service import ProductInfoService
from src.services.sheet_check_service import SheetCheckService
from src.utils.logger import setup_logger
from config.app_config import AppConfig

logger = setup_logger(__name__)

try:
    config = AppConfig.load_config()
except Exception:
    config = AppConfig.get_default_config()

file_repository = FileRepository(config)
google_sheets_repository = GoogleSheetsRepository(config)
api_client = ApiClient(config)
product_info_service = ProductInfoService(file_repository, api_client)
sheet_check_service = SheetCheckService(file_repository)

jan_code_controller = JanCodeController(
    product_info_service,
    sheet_check_service,
    google_sheets_repository
)

class JANCodeApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("JANコード等のコピー")
        self.root.geometry("400x500")
        
        window_position = os.environ.get('WINDOW_POSITION', '100,100')
        x, y = map(int, window_position.split(','))
        self.root.geometry(f"400x500+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(main_frame, text="JANコード等のコピー", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        self.jan_code_entry = ctk.CTkEntry(main_frame, placeholder_text="JANコードを入力")
        self.jan_code_entry.pack(pady=5, padx=10, fill="x")
        
        copy_button = ctk.CTkButton(main_frame, text="JANコードをコピー", command=self.copy_jan_code)
        copy_button.pack(pady=5)
        
        self.status_text = ctk.CTkTextbox(main_frame, height=200)
        self.status_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.update_status("アプリケーションが起動しました。")
        
    def get_jan_codes(self):
        """JANコードのリストを取得"""
        try:
            return jan_code_controller.get_jan_codes_from_sheets()
        except Exception as e:
            messagebox.showerror("エラー", f"JANコードの取得に失敗しました: {str(e)}")
            return []

    def get_jan_code_by_index(self, index):
        """指定されたインデックスのJANコードを取得"""
        try:
            return jan_code_controller.get_jan_code_by_index(index)
        except Exception as e:
            messagebox.showerror("エラー", f"JANコードの取得に失敗しました: {str(e)}")
            return None
    
    def copy_jan_code(self):
        """JANコードをクリップボードにコピー"""
        jan_code = self.jan_code_entry.get()
        if jan_code:
            try:
                pyperclip.copy(jan_code)
                self.update_status(f"JANコード {jan_code} をクリップボードにコピーしました。")
            except Exception as e:
                self.update_status(f"コピーに失敗しました: {str(e)}")
        else:
            messagebox.showwarning("警告", "JANコードを入力してください。")
    
    def update_status(self, message):
        """ステータステキストを更新"""
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = JANCodeApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        messagebox.showerror("アプリケーションエラー", f"アプリケーションの実行中にエラーが発生しました: {str(e)}")
