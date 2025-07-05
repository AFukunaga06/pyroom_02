# JANコード管理システム アーキテクチャ設計書

## 1. システム概要

JANコード管理システムは、商品検品・在庫管理・伝票作成業務を効率化するためのデスクトップアプリケーションです。

### 1.1 設計原則

- **関心の分離**: 各層が明確な責任を持つ
- **依存性の逆転**: 上位層が下位層に依存しない
- **単一責任の原則**: 各クラスが単一の責任を持つ
- **開放閉鎖の原則**: 拡張に開放、修正に閉鎖

## 2. アーキテクチャ概要

### 2.1 4層アーキテクチャ

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│        (GUI - CustomTkinter)           │
├─────────────────────────────────────────┤
│            Controller Layer             │
│     (Event Handling & Coordination)    │
├─────────────────────────────────────────┤
│             Service Layer               │
│         (Business Logic)               │
├─────────────────────────────────────────┤
│            Repository Layer             │
│        (Data Access & External)        │
└─────────────────────────────────────────┘
```

### 2.2 データフロー

```
User Input → GUI → Controller → Service → Repository → External System
                ↓       ↓         ↓          ↓
            Status   Business   Data      File/API
            Update   Logic    Processing  Operations
```

## 3. 各層の詳細設計

### 3.1 Presentation Layer (GUI)

**責任**: ユーザーインターフェースの提供

**主要コンポーネント**:
- `ctkmain_20250701_01.py`: メインウィンドウ
- `jancoordcopy1122_01aaa.py`: JANコードコピーサブアプリ
- `ckt0412sab01.py`: 廃番処理サブフォーム

**特徴**:
- CustomTkinterを使用した日本語対応GUI
- 15ボタンのグリッドレイアウト
- 色分けによる機能分類
- リアルタイムステータス表示

### 3.2 Controller Layer

**責任**: GUIイベントの処理とサービス層の調整

**主要クラス**:
- `MainController`: 全体的な制御
- `JanCodeController`: JANコード専用操作
- `CoordinateController`: 座標キャプチャ制御

**パターン**:
- Command Pattern: ボタンアクションの抽象化
- Observer Pattern: ステータス更新の通知

### 3.3 Service Layer

**責任**: ビジネスロジックの実装

**主要サービス**:

#### JanCoordService
- 座標キャプチャ
- クリップボード操作
- 画面領域取得

#### ProductInfoService
- JANコード抽出
- 商品情報取得
- データ変換

#### SheetCheckService
- 重複検出
- データ検証
- レポート生成

#### FileManagementService
- バッチファイル実行
- ファイル操作
- バックアップ管理

### 3.4 Repository Layer

**責任**: データアクセスの抽象化

**主要リポジトリ**:

#### FileRepository
- ローカルファイル操作
- テキストファイル読み書き
- ファイル存在確認

#### GoogleSheetsRepository
- Google Sheets API連携
- 認証管理
- データ取得・更新

#### ApiClient
- 外部API呼び出し
- リトライ機能
- エラーハンドリング

## 4. データモデル

### 4.1 主要エンティティ

```python
@dataclass
class Config:
    """アプリケーション設定"""
    api_key: str
    input_path: str
    output_path: str
    # ...

@dataclass
class ProductInfo:
    """商品情報"""
    jan: str
    name: str
    price: float
    # ...

@dataclass
class CheckReport:
    """チェック結果"""
    duplicates: List[str]
    missing: Dict[str, List[int]]
    # ...
```

### 4.2 例外階層

```
AppError
├── FileOperationError
├── APIError
└── ValidationError
```

## 5. 外部システム連携

### 5.1 Google Sheets API

**認証方式**: Service Account
**スコープ**: 
- `https://spreadsheets.google.com/feeds`
- `https://www.googleapis.com/auth/drive`

**操作**:
- レコード取得
- セル更新
- 行追加

### 5.2 商品情報API

**プロトコル**: REST API
**認証**: API Key
**リトライ**: 最大3回

### 5.3 ファイルシステム

**対象ファイル**:
- `input.txt`: タブ区切り形式
- `output.txt`: 処理結果
- `checkd01.txt`: 重複チェック結果
- `checkd02.txt`: データ検証結果

## 6. エラーハンドリング戦略

### 6.1 エラー分類

1. **システムエラー**: ファイル不存在、ネットワーク障害
2. **ビジネスエラー**: データ形式不正、重複検出
3. **ユーザーエラー**: 入力値不正、操作ミス

### 6.2 エラー処理フロー

```
Error Occurrence
       ↓
   Log Error
       ↓
  Classify Error
       ↓
Show User Message
       ↓
  Recovery Action
```

## 7. ログ戦略

### 7.1 ログレベル

- **DEBUG**: 詳細な実行情報
- **INFO**: 一般的な実行情報
- **WARNING**: 警告事項
- **ERROR**: エラー情報

### 7.2 ログ出力先

- **ファイル**: `logs/jancode_system_YYYYMMDD.log`
- **コンソール**: 開発時のデバッグ用

## 8. 設定管理

### 8.1 設定ファイル

**場所**: `config/config.json`
**形式**: JSON

**設定項目**:
- ファイルパス
- API設定
- Google Sheets設定
- ログレベル

### 8.2 デフォルト設定

アプリケーション内にハードコードされたデフォルト値を提供し、設定ファイルが存在しない場合でも動作可能。

## 9. テスト戦略

### 9.1 テスト分類

- **単体テスト**: 各サービス・リポジトリの個別テスト
- **統合テスト**: 層間の連携テスト
- **E2Eテスト**: GUI操作を含む全体テスト

### 9.2 モック戦略

- 外部API呼び出しのモック化
- ファイルシステム操作のモック化
- Google Sheets APIのモック化

## 10. パフォーマンス考慮事項

### 10.1 非同期処理

- バッチファイル実行の非同期化
- API呼び出しの非同期化
- GUI応答性の維持

### 10.2 キャッシュ戦略

- Google Sheetsデータのキャッシュ
- 商品情報のキャッシュ
- 設定情報のキャッシュ

## 11. セキュリティ考慮事項

### 11.1 認証情報管理

- Google API認証情報の安全な保存
- API Keyの環境変数化
- 認証情報のGit管理除外

### 11.2 入力検証

- JANコード形式の検証
- ファイルパスの検証
- 座標値の範囲チェック

## 12. 拡張性

### 12.1 新機能追加

- 新しいサービスクラスの追加
- 新しいリポジトリの追加
- 新しいデータモデルの追加

### 12.2 外部システム連携

- 新しいAPI連携の追加
- 新しいファイル形式のサポート
- 新しい認証方式のサポート

## 13. 運用・保守

### 13.1 ログ監視

- エラーログの定期確認
- パフォーマンスログの分析
- 使用状況の把握

### 13.2 バックアップ

- 設定ファイルのバックアップ
- データファイルのバックアップ
- ログファイルのローテーション

この設計により、保守性・拡張性・テスト容易性を確保した堅牢なシステムを実現しています。
