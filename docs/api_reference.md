# JANコード管理システム API リファレンス

## Service Layer API

### JanCoordService

JANコード座標取得サービス

#### メソッド

##### `capture_coordinates() -> Tuple[int, int]`
現在のマウス位置を取得し、座標をファイルに記録します。

**戻り値:**
- `Tuple[int, int]`: (x, y) 座標

**例外:**
- `AppError`: 座標取得に失敗した場合

##### `copy_last_coordinate_to_clipboard() -> str`
最後に取得した座標をクリップボードに転送します。

**戻り値:**
- `str`: クリップボードにコピーされたデータ

##### `capture_screen_region(start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> str`
指定された範囲の画面をキャプチャします。

**パラメータ:**
- `start_pos`: 開始座標
- `end_pos`: 終了座標

**戻り値:**
- `str`: キャプチャ結果の説明

### ProductInfoService

商品情報抽出サービス

#### メソッド

##### `extract_product_info() -> List[ProductInfo]`
input.txtからJANコードを抽出し、商品情報を取得します。

**戻り値:**
- `List[ProductInfo]`: 商品情報のリスト

##### `process_clipboard_data(jan_code: str, clipboard_data: str) -> None`
クリップボードデータを処理してinput.txtに追加します。

**パラメータ:**
- `jan_code`: JANコード
- `clipboard_data`: クリップボードのデータ

##### `add_discontinued_product(jan_code: str) -> None`
廃番商品をinput.txtに追加します。

**パラメータ:**
- `jan_code`: 廃番商品のJANコード

### SheetCheckService

シートチェックサービス

#### メソッド

##### `check_duplicates_and_missing() -> CheckReport`
重複と項目抜けのチェックを実行します。

**戻り値:**
- `CheckReport`: チェック結果レポート

##### `get_jan_code_count_and_current() -> Tuple[int, str]`
JANコードの総数と現在のJANコードを取得します。

**戻り値:**
- `Tuple[int, str]`: (総数, 現在のJANコード)

### FileManagementService

ファイル管理サービス

#### メソッド

##### `execute_batch_file(batch_file_path: str) -> bool`
バッチファイルを実行します。

**パラメータ:**
- `batch_file_path`: バッチファイルのパス

**戻り値:**
- `bool`: 実行成功の可否

##### `open_file(file_path: str) -> bool`
ファイルを開きます。

**パラメータ:**
- `file_path`: 開くファイルのパス

**戻り値:**
- `bool`: 実行成功の可否

## Repository Layer API

### FileRepository

ファイル操作リポジトリ

#### メソッド

##### `read_input_file() -> str`
input.txtの内容を読み取ります。

**戻り値:**
- `str`: ファイルの内容

##### `append_to_input(data: str) -> None`
input.txtにデータを追記します。

**パラメータ:**
- `data`: 追記するデータ

##### `write_output(data: str) -> None`
output.txtにデータを書き込みます。

**パラメータ:**
- `data`: 書き込むデータ

##### `write_checkd_file(file_type: str, data: str) -> None`
checkdファイルにデータを書き込みます。

**パラメータ:**
- `file_type`: ファイルタイプ ('checkd01' または 'checkd02')
- `data`: 書き込むデータ

### GoogleSheetsRepository

Google Sheets操作リポジトリ

#### メソッド

##### `get_all_records() -> List[Dict[str, Any]]`
シートからすべてのレコードを取得します。

**戻り値:**
- `List[Dict[str, Any]]`: レコードのリスト

##### `get_jan_codes() -> List[str]`
シートからJANコードのリストを取得します。

**戻り値:**
- `List[str]`: JANコードのリスト

##### `update_cell(row: int, col: int, value: str) -> None`
指定されたセルを更新します。

**パラメータ:**
- `row`: 行番号
- `col`: 列番号
- `value`: 設定する値

### ApiClient

外部API呼び出しクライアント

#### メソッド

##### `query_product_info(jan_code: str) -> Optional[ProductInfo]`
JANコードから商品情報を取得します。

**パラメータ:**
- `jan_code`: JANコード

**戻り値:**
- `Optional[ProductInfo]`: 商品情報（見つからない場合はNone）

##### `validate_jan_code(jan_code: str) -> bool`
JANコードの形式を検証します。

**パラメータ:**
- `jan_code`: 検証するJANコード

**戻り値:**
- `bool`: 有効な形式かどうか

## Controller Layer API

### MainController

メインコントローラ

#### メソッド

##### `capture_jan_coordinates() -> bool`
JAN座標取得を実行します。

**戻り値:**
- `bool`: 実行成功の可否

##### `copy_jan_code() -> bool`
JANコードコピーを実行します。

**戻り値:**
- `bool`: 実行成功の可否

##### `extract_product_info() -> bool`
商品情報抽出を実行します。

**戻り値:**
- `bool`: 実行成功の可否

##### `check_sheet_data() -> Optional[CheckReport]`
シートチェックを実行します。

**戻り値:**
- `Optional[CheckReport]`: チェック結果（失敗時はNone）

##### `execute_batch_operation() -> bool`
一括実行を実行します。

**戻り値:**
- `bool`: 実行成功の可否

## Data Models

### Config

アプリケーション設定

#### フィールド

- `api_key: str` - API キー
- `input_path: str` - 入力ファイルパス
- `output_path: str` - 出力ファイルパス
- `checkd01_path: str` - チェック結果ファイル1のパス
- `checkd02_path: str` - チェック結果ファイル2のパス
- `google_credentials_path: str` - Google認証情報ファイルパス
- `spreadsheet_id: str` - Google SheetsのスプレッドシートID

### ProductInfo

商品情報

#### フィールド

- `jan: str` - JANコード
- `name: str` - 商品名
- `price: float` - 価格
- `brand: str` - ブランド名
- `retrieved_at: datetime` - 取得日時
- `is_discontinued: bool` - 廃番フラグ

### CheckReport

チェック結果レポート

#### フィールド

- `duplicates: List[str]` - 重複JANコードのリスト
- `missing: Dict[str, List[int]]` - 欠損フィールドの情報
- `discontinued: List[str]` - 廃番JANコードのリスト
- `total_records: int` - 総レコード数
- `check_timestamp: datetime` - チェック実行日時

### JANCodeData

JANコードデータ

#### フィールド

- `jan_code: str` - JANコード
- `brand_name: Optional[str]` - ブランド名
- `product_name: Optional[str]` - 商品名
- `price: Optional[float]` - 価格
- `is_discontinued: bool` - 廃番フラグ
- `line_number: Optional[int]` - 行番号

## 例外クラス

### AppError

アプリケーション固有のエラーの基底クラス

### FileOperationError

ファイル操作エラー

### APIError

API呼び出しエラー

### ValidationError

データ検証エラー

## 使用例

### 基本的な使用方法

```python
from config.app_config import AppConfig
from src.controllers.main_controller import MainController

config = AppConfig.load_config()
controller = MainController(config)

success = controller.capture_jan_coordinates()
if success:
    print("座標取得が完了しました")

success = controller.extract_product_info()
if success:
    print("商品情報抽出が完了しました")

report = controller.check_sheet_data()
if report:
    print(f"重複: {len(report.duplicates)}件")
    print(f"廃番: {len(report.discontinued)}件")
```

### エラーハンドリング

```python
try:
    controller.extract_product_info()
except AppError as e:
    print(f"アプリケーションエラー: {e}")
except Exception as e:
    print(f"予期しないエラー: {e}")
```

### カスタム設定

```python
from src.models.data_models import Config

config = Config(
    api_key="your_api_key",
    input_path="custom_input.txt",
    output_path="custom_output.txt",
    checkd01_path="custom_checkd01.txt",
    checkd02_path="custom_checkd02.txt",
    google_credentials_path="your_credentials.json",
    spreadsheet_id="your_spreadsheet_id"
)
```
