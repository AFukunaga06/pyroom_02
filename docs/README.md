# JANコード管理システム

## 概要

JANコードやシート上のデータを自動抽出・チェックし、その結果をテキスト出力・クリップボード転送・GUI表示でユーザーに提供するシステムです。

## アーキテクチャ

本システムは以下の4層アーキテクチャで構成されています：

```
GUI (Presentation) → Controller → Service → Repository → External APIs/Files
```

### 層の説明

- **Presentation Layer (GUI)**: CustomTkinterを使用したユーザーインターフェース
- **Controller Layer**: GUIからの要求を受け取り、適切なサービスを呼び出す
- **Service Layer**: ビジネスロジックを実装
- **Repository Layer**: データアクセスを抽象化（ファイル、Google Sheets、外部API）

## 主要機能

1. **JANコード座標取得**: マウス位置を取得し、座標をテキストファイルに記録
2. **JANコードコピー**: 指定範囲のテキストをクリップボードへ転送
3. **商品情報抽出**: 外部APIへ問い合わせ、商品名・価格などを取得
4. **シートチェック**: 重複・欠損・フォーマット不備を検出
5. **GUI一括実行**: 上記各機能をワンクリックで順次実行

## ディレクトリ構成

```
pyroom_02/
├── src/
│   ├── gui/                    # GUI コンポーネント
│   ├── controllers/            # コントローラ層
│   ├── services/              # サービス層
│   ├── repositories/          # リポジトリ層
│   ├── models/                # データモデル
│   ├── utils/                 # ユーティリティ
│   └── scripts/               # 外部スクリプト
├── config/                    # 設定ファイル
├── tests/                     # テストファイル
├── docs/                      # ドキュメント
├── logs/                      # ログファイル
├── requirements.txt           # 依存関係
├── ctkmain_20250701_01.py    # メインアプリケーション
├── jancoordcopy1122_01aaa.py # JANコードコピーサブアプリ
├── ckt0412sab01.py           # 廃番処理サブフォーム
└── *.bat                     # バッチファイル
```

## セットアップ

### 必要な環境

- Python 3.10以降
- Windows 10以降（推奨）

### インストール

1. 依存関係をインストール：
```bash
python install_dependencies.py
```
または
```bash
pip install -r requirements.txt
```

2. Google API認証情報を配置：
   - `samplep20240906-5ae36c9a4acd.json` をプロジェクトルートに配置

3. 設定ファイルを確認：
   - `config/config.json` で設定をカスタマイズ可能

## 使用方法

### メインアプリケーションの起動

```bash
python ctkmain_20250701_01.py
```

### 主要ボタンの説明

- **重複と項目抜けのチェック**: データの重複や欠損をチェック
- **JANコード等のコピー**: JANコードコピーサブアプリを起動
- **廃番処理サブフォーム**: 廃番商品登録フォームを起動
- **貼り付けて実行**: クリップボードデータを処理
- **座標取得**: マウス座標をキャプチャ
- **一括実行**: 全機能を順次実行

## データファイル

- `input.txt`: 入力データ（JANコード、商品情報等）
- `output.txt`: 処理結果出力
- `checkd01.txt`: 重複チェック結果
- `checkd02.txt`: データ検証結果

## 外部連携

- **Google Sheets**: スプレッドシートID `17Le1KA9nzMREt0Qp9_elM1OF1q8aSp-GDBZRPOntNI8`
- **商品情報API**: JANコードから商品情報を取得
- **クリップボード**: データの転送・取得

## エラー処理

- 全層で包括的なエラーハンドリングを実装
- ログファイルによる詳細な実行記録
- ユーザーフレンドリーな日本語エラーメッセージ

## 開発者向け情報

### テスト実行

```bash
python run_tests.py
```
または
```bash
pytest tests/
```

### ログ確認

ログファイルは `logs/` ディレクトリに日付別で保存されます。

### 設定のカスタマイズ

`config/config.json` で各種設定をカスタマイズできます：

```json
{
  "input_path": "input.txt",
  "output_path": "output.txt",
  "checkd01_path": "checkd01.txt",
  "checkd02_path": "checkd02.txt",
  "google_credentials_path": "samplep20240906-5ae36c9a4acd.json",
  "spreadsheet_id": "17Le1KA9nzMREt0Qp9_elM1OF1q8aSp-GDBZRPOntNI8"
}
```

## トラブルシューティング

### よくある問題

1. **Google Sheets接続エラー**
   - 認証情報ファイルのパスを確認
   - インターネット接続を確認

2. **座標取得が動作しない**
   - pyautoguiの権限を確認
   - セキュリティソフトの設定を確認

3. **ファイルが見つからない**
   - 作業ディレクトリを確認
   - ファイルパスの設定を確認

## ライセンス

このプロジェクトは内部使用を目的としています。
