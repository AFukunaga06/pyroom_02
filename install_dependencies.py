#!/usr/bin/env python3
"""
依存関係インストールスクリプト
"""
import sys
import subprocess
import os

def install_dependencies():
    """依存関係をインストール"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(project_root, 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("❌ requirements.txt が見つかりません")
        return False
    
    try:
        print("📦 依存関係をインストール中...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', requirements_file
        ], check=True)
        print("✅ 依存関係のインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False
    except Exception as e:
        print(f"❌ インストール中にエラーが発生しました: {e}")
        return False

def main():
    """メイン関数"""
    if install_dependencies():
        print("\n🚀 セットアップが完了しました。以下のコマンドでアプリケーションを起動できます:")
        print("python ctkmain_20250701_01.py")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
