# JANコード管理システム デプロイメントガイド

## 概要

このドキュメントでは、JANコード管理システムを様々な環境にデプロイする方法について説明します。

## 前提条件

- Python 3.10以上
- Git
- Google Sheets API認証情報

## ローカル環境でのセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/AFukunaga06/pyroom_02.git
cd pyroom_02
```

### 2. 依存関係のインストール

```bash
python install_dependencies.py
```

または

```bash
pip install -r requirements.txt
```

### 3. 設定ファイルの準備

Google API認証情報ファイル `samplep20240906-5ae36c9a4acd.json` をプロジェクトルートに配置してください。

### 4. アプリケーションの起動

```bash
python ctkmain_20250701_01.py
```

または

```bash
python main.py
```

## VPSサーバーでのデプロイ

### Ubuntu/Debian系

```bash
# システムの更新
sudo apt update && sudo apt upgrade -y

# Python 3.10のインストール
sudo apt install python3.10 python3.10-pip python3.10-venv -y

# プロジェクトのクローン
git clone https://github.com/AFukunaga06/pyroom_02.git
cd pyroom_02

# 仮想環境の作成
python3.10 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# Google API認証情報の配置
# samplep20240906-5ae36c9a4acd.json をアップロード

# アプリケーションの起動
python ctkmain_20250701_01.py
```

### CentOS/RHEL系

```bash
# システムの更新
sudo yum update -y

# Python 3.10のインストール
sudo yum install python3.10 python3.10-pip -y

# プロジェクトのクローン
git clone https://github.com/AFukunaga06/pyroom_02.git
cd pyroom_02

# 仮想環境の作成
python3.10 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# Google API認証情報の配置
# samplep20240906-5ae36c9a4acd.json をアップロード

# アプリケーションの起動
python ctkmain_20250701_01.py
```

## Dockerでのデプロイ

### Dockerfileの作成

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "ctkmain_20250701_01.py"]
```

### Docker Composeでのデプロイ

```yaml
version: '3.8'

services:
  jancode-system:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped
```

### ビルドと起動

```bash
docker-compose up -d
```

## クラウドサービスでのデプロイ

### AWS EC2

1. EC2インスタンスを作成（Ubuntu 20.04 LTS推奨）
2. セキュリティグループで必要なポートを開放
3. SSH接続してVPSサーバーでのデプロイ手順を実行

### Google Cloud Platform

1. Compute Engineインスタンスを作成
2. ファイアウォールルールを設定
3. SSH接続してVPSサーバーでのデプロイ手順を実行

### Microsoft Azure

1. Virtual Machineを作成
2. ネットワークセキュリティグループを設定
3. SSH接続してVPSサーバーでのデプロイ手順を実行

## 共有ホスティングでのデプロイ

### cPanelを使用する場合

1. ファイルマネージャーでプロジェクトファイルをアップロード
2. Python Appを作成
3. 依存関係をインストール
4. アプリケーションを起動

### Pleskを使用する場合

1. Git経由でプロジェクトをデプロイ
2. Python環境を設定
3. 依存関係をインストール
4. アプリケーションを起動

## 環境変数の設定

以下の環境変数を設定することで、アプリケーションの動作をカスタマイズできます：

```bash
export PYTHONPATH=/path/to/pyroom_02
export LOG_LEVEL=INFO
export CONFIG_PATH=/path/to/config.json
```

## ログの設定

ログファイルは `logs/` ディレクトリに出力されます：

- `app.log`: アプリケーションログ
- `error.log`: エラーログ
- `debug.log`: デバッグログ

## バックアップとリストア

### データファイルのバックアップ

```bash
# 重要なデータファイルをバックアップ
cp input.txt backup/input_$(date +%Y%m%d).txt
cp output.txt backup/output_$(date +%Y%m%d).txt
cp checkd01.txt backup/checkd01_$(date +%Y%m%d).txt
cp checkd02.txt backup/checkd02_$(date +%Y%m%d).txt
```

### 設定ファイルのバックアップ

```bash
cp config/config.json backup/config_$(date +%Y%m%d).json
cp samplep20240906-5ae36c9a4acd.json backup/credentials_$(date +%Y%m%d).json
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. Google Sheets APIエラー

```
解決方法:
- 認証情報ファイルが正しく配置されているか確認
- Google Cloud Consoleでシート共有設定を確認
- APIクォータ制限を確認
```

#### 2. ファイル権限エラー

```bash
# ファイル権限を修正
chmod 644 *.txt
chmod 755 *.py
chmod 755 *.bat
```

#### 3. 依存関係エラー

```bash
# 仮想環境を再作成
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. 文字化け問題

```bash
# 環境変数を設定
export LANG=ja_JP.UTF-8
export LC_ALL=ja_JP.UTF-8
```

## パフォーマンス最適化

### メモリ使用量の最適化

- 大きなファイルを処理する際は、チャンク読み込みを使用
- 不要なオブジェクトは適切に削除

### 処理速度の最適化

- Google Sheets APIの呼び出し回数を最小限に抑制
- キャッシュ機能を活用

## セキュリティ考慮事項

### 認証情報の保護

- Google API認証情報ファイルは適切な権限で保護
- 本番環境では環境変数を使用

### ファイルアクセス制御

- データファイルへのアクセス権限を適切に設定
- ログファイルの権限を制限

## 監視とメンテナンス

### ログ監視

```bash
# リアルタイムでログを監視
tail -f logs/app.log
```

### システムリソース監視

```bash
# CPU・メモリ使用量を確認
top
htop
```

### 定期メンテナンス

- ログファイルのローテーション
- データファイルのバックアップ
- 依存関係の更新確認

## サポート

問題が発生した場合は、以下の情報を含めてサポートに連絡してください：

1. エラーメッセージ
2. ログファイルの内容
3. 実行環境の詳細
4. 再現手順

## 更新手順

### アプリケーションの更新

```bash
# 最新版を取得
git pull origin main

# 依存関係を更新
pip install -r requirements.txt --upgrade

# アプリケーションを再起動
python ctkmain_20250701_01.py
```

### データベースマイグレーション

新しいバージョンでデータ形式が変更された場合は、マイグレーションスクリプトを実行してください。

## ライセンス

このソフトウェアは MIT ライセンスの下で提供されています。
