import customtkinter
import tkinter.messagebox as messagebox
import os
import sys
import subprocess
import threading
from src.models.data_models import Config, AppError
from src.controllers.main_controller import MainController
from src.controllers.jan_code_controller import JanCodeController
from src.controllers.coordinate_controller import CoordinateController
from src.utils.logger import setup_logger
from config.app_config import AppConfig

logger = setup_logger(__name__)

try:
    config = AppConfig.load_config()
except Exception:
    config = AppConfig.get_default_config()

main_controller = MainController(config)
jan_code_controller = JanCodeController(
    main_controller.product_info_service,
    main_controller.sheet_check_service,
    main_controller.google_sheets_repository
)
coordinate_controller = CoordinateController(main_controller.jan_coord_service)

def show_under_construction():
    messagebox.showinfo("お知らせ", "この機能は現在工事中です。\nしばらくお待ちください。")

def update_status(message):
    """ステータスを更新"""
    if hasattr(window, 'output'):
        window.output.insert(customtkinter.END, f"{message}\n")
        window.output.see(customtkinter.END)

def show_error(message):
    """エラーを表示"""
    messagebox.showerror("エラー", message)

main_controller.set_status_callback(update_status)
main_controller.set_error_callback(show_error)

def check_and_count_jan_codes():
    """重複と項目抜けのチェック"""
    try:
        report = main_controller.check_sheet_data()
        if report:
            window.output.delete("1.0", customtkinter.END)
            
            if report.duplicates:
                for duplicate in report.duplicates:
                    window.output.insert(customtkinter.END, f"JANコード {duplicate} が重複しています\n")
            else:
                window.output.insert(customtkinter.END, "重複はありません\n")
            
            for code in report.discontinued:
                window.output.insert(customtkinter.END, f"JANコード {code} は廃番です\n")
            
            window.output.insert(customtkinter.END, f"JANコードは上から{report.total_records}番目です\n", "red_text")
            
            count, current = jan_code_controller.get_current_jan_code_info()
            if current:
                window.output.insert(customtkinter.END, f"現在のJANコードは{current}です\n")
            
            window.output.tag_config("red_text", foreground="red")
    except Exception as e:
        show_error(f"チェック処理中にエラーが発生しました: {str(e)}")

def paste_and_execute():
    """クリップボードデータを処理"""
    try:
        success = main_controller.process_clipboard_data()
        if success:
            update_status("クリップボードデータを処理しました")
    except Exception as e:
        show_error(f"クリップボード処理中にエラーが発生しました: {str(e)}")

def open_file(file_path):
    """ファイルを開く"""
    try:
        main_controller.open_file(file_path)
    except Exception as e:
        show_error(f"ファイルを開く際にエラーが発生しました: {str(e)}")

def execute_batch_and_open_file(batch_file, output_file):
    """バッチファイルを実行してファイルを開く"""
    try:
        main_controller.execute_batch_file(batch_file, output_file)
    except Exception as e:
        show_error(f"バッチファイル実行中にエラーが発生しました: {str(e)}")

def open_jancoordcopy():
    """JANコード等のコピーサブアプリを開く"""
    try:
        os.environ['WINDOW_POSITION'] = f"{window.winfo_x() + window.winfo_width() + 10},{window.winfo_y()}"
        subprocess.Popen([sys.executable, 'jancoordcopy1122_01aaa.py'])
    except Exception as e:
        show_error(f"JANコード等のコピーアプリの起動に失敗しました: {str(e)}")

def open_ckt0412sab01():
    """廃番処理サブフォームを開く"""
    try:
        subprocess.Popen([sys.executable, 'ckt0412sab01.py'])
    except Exception as e:
        show_error(f"廃番処理サブフォームの起動に失敗しました: {str(e)}")

def open_url(url):
    """URLを開く"""
    try:
        if os.name == 'nt':
            subprocess.run(['start', url], shell=True)
        else:
            subprocess.run(['xdg-open', url])
    except Exception as e:
        show_error(f"URLを開く際にエラーが発生しました: {str(e)}")

def capture_coordinates():
    """座標を取得"""
    try:
        main_controller.capture_jan_coordinates()
    except Exception as e:
        show_error(f"座標取得中にエラーが発生しました: {str(e)}")

def copy_jan_code():
    """JANコードをコピー"""
    try:
        main_controller.copy_jan_code()
    except Exception as e:
        show_error(f"JANコードコピー中にエラーが発生しました: {str(e)}")

def extract_product_info():
    """商品情報を抽出"""
    try:
        main_controller.extract_product_info()
    except Exception as e:
        show_error(f"商品情報抽出中にエラーが発生しました: {str(e)}")

def batch_execute():
    """一括実行"""
    try:
        main_controller.execute_batch_operation()
    except Exception as e:
        show_error(f"一括実行中にエラーが発生しました: {str(e)}")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("JANコード管理システム")
window.geometry("600x700")

frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=20, padx=20, fill="both", expand=True)

button_frame = customtkinter.CTkFrame(master=frame)
button_frame.pack(pady=10, padx=10, fill="x")

buttons = [
    ("重複と項目抜けのチェック", check_and_count_jan_codes),
    ("JANコード等のコピー", open_jancoordcopy),
    ("廃番処理サブフォーム", open_ckt0412sab01),
    ("貼り付けて実行", paste_and_execute),
    ("チェックシート", lambda: open_url("https://docs.google.com/spreadsheets/d/17Le1KA9nzMREt0Qp9_elM1OF1q8aSp-GDBZRPOntNI8/edit?gid=0#gid=0")),
    ("商品n", lambda: open_url("https://docs.google.com/spreadsheets/d/1qehObPI2ZB73BaqOEvgBmOVQy6V9yUhZUCQ2UeKo8b8/edit#gid=1363197529")),
    ("藤原産業", lambda: open_url("https://www.fujiwarasangyo-markeweb2.com/")),
    ("Type1", lambda: execute_batch_and_open_file("Type1x.bat", "checkd02.txt")),
    ("Type2", lambda: execute_batch_and_open_file("Type2x.bat", "output.txt")),
    ("input.txt", lambda: open_file("input.txt")),
    ("output.txt", lambda: open_file("output.txt")),
    ("checkd01.txt", lambda: open_file("checkd01.txt")),
    ("checkd02.txt", lambda: open_file("checkd02.txt")),
    ("座標取得", capture_coordinates),
    ("一括実行", batch_execute)
]

for i, (text, command) in enumerate(buttons):
    row = i // 3
    col = i % 3
    
    if text == "重複と項目抜けのチェック":
        color = "red"
    elif text in ["JANコード等のコピー", "廃番処理サブフォーム"]:
        color = "green"
    elif text == "貼り付けて実行":
        color = "orange"
    elif text in ["座標取得", "一括実行"]:
        color = "purple"
    else:
        color = "blue"
    
    button = customtkinter.CTkButton(
        master=button_frame,
        text=text,
        command=command,
        fg_color=color,
        width=180,
        height=40
    )
    button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

for col in range(3):
    button_frame.grid_columnconfigure(col, weight=1)

output_frame = customtkinter.CTkFrame(master=frame)
output_frame.pack(pady=10, padx=10, fill="both", expand=True)

output_label = customtkinter.CTkLabel(master=output_frame, text="出力:")
output_label.pack(pady=(10, 5))

window.output = customtkinter.CTkTextbox(master=output_frame, height=200)
window.output.pack(pady=5, padx=10, fill="both", expand=True)

if __name__ == "__main__":
    try:
        logger.info("Starting JANコード管理システム")
        window.mainloop()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        messagebox.showerror("アプリケーションエラー", f"アプリケーションの実行中にエラーが発生しました: {str(e)}")
    finally:
        logger.info("JANコード管理システム terminated")
