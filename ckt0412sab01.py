import customtkinter as ctk
import pyperclip
from tkinter import messagebox

def add_to_file():
    jan_code = entry.get()
    if not jan_code:
        messagebox.showwarning("警告", "JANコードを入力してください。")
        return
    
    try:
        from src.controllers.main_controller import MainController
        from config.app_config import AppConfig
        
        config = AppConfig.get_default_config()
        controller = MainController(config)
        
        success = controller.add_discontinued_product(jan_code)
        if success:
            pyperclip.copy(f"JANコード\t{jan_code}\nブランド名\t廃番\n")
            entry.delete(0, ctk.END)
            messagebox.showinfo("完了", "廃番商品を追加しました。")
        else:
            messagebox.showerror("エラー", "廃番商品の追加に失敗しました。")
    except Exception as e:
        messagebox.showerror("エラー", f"処理中にエラーが発生しました: {str(e)}")

root = ctk.CTk()
root.title("廃番処理サブフォーム")
root.geometry("300x150")

frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

label = ctk.CTkLabel(frame, text="JANコードを入力してください:")
label.pack(pady=10)

entry = ctk.CTkEntry(frame, placeholder_text="JANコード")
entry.pack(pady=5, padx=10, fill="x")

button = ctk.CTkButton(frame, text="廃番として追加", command=add_to_file)
button.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
