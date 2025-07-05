#!/usr/bin/env python3
"""
Test runner for JANコード管理システム
"""
import sys
import os
import subprocess

def main():
    """テストを実行"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v', 
            '--tb=short',
            '--color=yes'
        ], check=True)
        print("✅ すべてのテストが成功しました")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ テストが失敗しました: {e}")
        return 1
    except Exception as e:
        print(f"❌ テスト実行中にエラーが発生しました: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
