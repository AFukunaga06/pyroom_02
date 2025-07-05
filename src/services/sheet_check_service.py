"""
Sheet checking and validation service.
"""
import re
from collections import Counter
from typing import List, Dict, Tuple
from ..models.data_models import CheckReport, JANCodeData, AppError
from ..repositories.file_repository import FileRepository
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SheetCheckService:
    """シートチェックサービス"""
    
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
    
    def check_duplicates_and_missing(self) -> CheckReport:
        """重複と項目抜けのチェック"""
        try:
            logger.info("Starting sheet check for duplicates and missing items")
            
            input_content = self.file_repository.read_input_file()
            jan_codes = self._extract_jan_codes_with_context(input_content)
            
            duplicates = self._find_duplicates(jan_codes)
            discontinued = self._find_discontinued_codes(input_content)
            missing = self._find_missing_fields(input_content)
            
            report = CheckReport(
                duplicates=duplicates,
                missing=missing,
                discontinued=discontinued,
                total_records=len(jan_codes),
                check_timestamp=datetime.now()
            )
            
            self._write_check_results(report)
            
            logger.info(f"Sheet check completed. Found {len(duplicates)} duplicates, {len(discontinued)} discontinued items")
            return report
            
        except Exception as e:
            logger.error(f"Failed to check sheet: {str(e)}")
            raise AppError(f"シートチェックに失敗しました: {str(e)}")
    
    def _extract_jan_codes_with_context(self, content: str) -> List[JANCodeData]:
        """JANコードとその関連データを抽出"""
        jan_codes = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            match = re.search(r'JANコード\t(\d+)', line)
            if match:
                jan_code = match.group(1)
                
                brand_name = None
                product_name = None
                
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    brand_match = re.search(r'ブランド名\t(.+)', next_line)
                    if brand_match:
                        brand_name = brand_match.group(1)
                
                jan_data = JANCodeData(
                    jan_code=jan_code,
                    brand_name=brand_name,
                    line_number=i + 1,
                    is_discontinued=(brand_name == '廃番' if brand_name else False)
                )
                jan_codes.append(jan_data)
        
        return jan_codes
    
    def _find_duplicates(self, jan_codes: List[JANCodeData]) -> List[str]:
        """重複するJANコードを検出"""
        code_counts = Counter(jan_data.jan_code for jan_data in jan_codes)
        return [code for code, count in code_counts.items() if count > 1]
    
    def _find_discontinued_codes(self, content: str) -> List[str]:
        """廃番コードを検出"""
        jan_codes = re.findall(r'JANコード\t(\d+)', content)
        discontinued_codes = []
        
        for code in jan_codes:
            if f'JANコード\t{code}' in content:
                code_section = content.split(f'JANコード\t{code}')[1].split('JANコード')[0]
                if 'ブランド名\t廃番' in code_section:
                    discontinued_codes.append(code)
        
        return discontinued_codes
    
    def _find_missing_fields(self, content: str) -> Dict[str, List[int]]:
        """欠損フィールドを検出"""
        missing = {'brand_name': [], 'product_name': []}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if re.search(r'JANコード\t(\d+)', line):
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not re.search(r'ブランド名\t', next_line):
                        missing['brand_name'].append(i + 1)
        
        return missing
    
    def _write_check_results(self, report: CheckReport) -> None:
        """チェック結果をファイルに書き込み"""
        checkd01_content = []
        checkd02_content = []
        
        if report.duplicates:
            checkd01_content.append("=== 重複JANコード ===")
            for duplicate in report.duplicates:
                checkd01_content.append(f"JANコード {duplicate} が重複しています")
        else:
            checkd01_content.append("重複はありません")
        
        if report.discontinued:
            checkd01_content.append("\n=== 廃番商品 ===")
            for code in report.discontinued:
                checkd01_content.append(f"JANコード {code} は廃番です")
        
        checkd01_content.append(f"\nJANコードは上から{report.total_records}番目です")
        
        if report.missing['brand_name']:
            checkd02_content.append("=== ブランド名欠損 ===")
            for line_num in report.missing['brand_name']:
                checkd02_content.append(f"行 {line_num}: ブランド名が欠損しています")
        
        self.file_repository.write_checkd_file('checkd01', '\n'.join(checkd01_content))
        self.file_repository.write_checkd_file('checkd02', '\n'.join(checkd02_content))
    
    def get_jan_code_count_and_current(self) -> Tuple[int, str]:
        """JANコードの総数と現在のJANコードを取得"""
        try:
            input_content = self.file_repository.read_input_file()
            jan_codes = re.findall(r'JANコード\t(\d+)', input_content)
            
            count = len(jan_codes)
            current = jan_codes[-1] if jan_codes else ""
            
            return count, current
            
        except Exception as e:
            logger.error(f"Failed to get JAN code count: {str(e)}")
            return 0, ""
