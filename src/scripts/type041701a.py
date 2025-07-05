"""
Type041701a.py - Replacement for missing external script referenced in Type1x.bat
This script performs data validation and outputs results to checkd02.txt
"""
import sys
import os
from datetime import datetime

def main():
    """メイン処理 - データ検証を実行してcheckd02.txtに出力"""
    try:
        input_file = 'input.txt'
        output_lines = []
        
        output_lines.append("=== データ検証結果 ===")
        output_lines.append(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("")
        
        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            jan_count = 0
            error_count = 0
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                
                if 'JANコード' in line:
                    jan_count += 1
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        jan_code = parts[1]
                        if not jan_code.isdigit():
                            output_lines.append(f"行 {i}: 無効なJANコード形式 - {jan_code}")
                            error_count += 1
                        elif len(jan_code) not in [8, 13]:
                            output_lines.append(f"行 {i}: JANコード桁数エラー - {jan_code}")
                            error_count += 1
            
            output_lines.append("")
            output_lines.append(f"検証完了: JANコード {jan_count}件, エラー {error_count}件")
            
        else:
            output_lines.append("エラー: input.txt が見つかりません")
        
        for line in output_lines:
            print(line)
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
