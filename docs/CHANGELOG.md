# Changelog

## [1.0.0] - 2025-01-02

### Added
- 完全な4層アーキテクチャの実装 (Presentation → Controller → Service → Repository)
- JANコード座標取得機能
- JANコードクリップボード操作機能
- 商品情報抽出機能
- シートチェック機能（重複・欠損検出）
- GUI一括実行機能
- Google Sheets API連携
- 包括的なエラーハンドリング
- 日本語対応ログシステム
- 設定管理システム
- 単体テスト・統合テスト
- 包括的なドキュメント

### Changed
- 既存のモノリシック構造から階層化アーキテクチャに移行
- Google API認証の改善
- ファイル操作の安全性向上
- エラーメッセージの日本語化

### Fixed
- バッチファイルのパス問題
- 座標取得の型安全性
- Google Sheets接続の安定性

### Technical Details
- Python 3.10+ 対応
- CustomTkinter GUI フレームワーク
- Google Sheets API v4
- 包括的なテストカバレッジ
- 型ヒント完全対応
- ログローテーション機能
