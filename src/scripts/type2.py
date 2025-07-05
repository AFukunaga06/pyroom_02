"""
Type2.py - Replacement for missing external script referenced in Type2x.bat
This script processes product information and outputs results to output.txt
"""
import sys
import os
import re
from datetime import datetime

def main():
    """メイン処理 - 商品情報を処理してoutput.txtに出力"""
    try:
        input_file = 'input.txt'
        output_lines = []
        
        output_lines.append("=== 商品情報処理結果 ===")
        output_lines.append(f"処理日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("")
        output_lines.append("JANコード\t商品名\t価格\t処理日時")
        
        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            jan_codes = re.findall(r'JANコード\t(\d+)', content)
            
            for jan_code in jan_codes:
                product_name = f"商品情報が見つかりませんでした。{jan_code}"
                price = "0"
                process_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                output_line = f"{jan_code}\t{product_name}\t{price}\t{process_time}"
                output_lines.append(output_line)
            
            output_lines.append("")
            output_lines.append(f"処理完了: {len(jan_codes)}件のJANコードを処理しました")
            
        else:
            output_lines.append("エラー: input.txt が見つかりません")
        
        for line in output_lines:
            print(line)
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
