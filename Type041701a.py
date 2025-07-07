import re
import sys

def extract_jan_codes():
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        jan_codes = re.findall(r'JANコード\t(\d+)', content)
        
        for code in jan_codes:
            print(code)
            
    except FileNotFoundError:
        print("input.txt not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    extract_jan_codes()
