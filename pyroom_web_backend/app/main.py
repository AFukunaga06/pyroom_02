from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import re
import tempfile
from collections import Counter
from typing import List, Optional
import gspread
from google.oauth2.service_account import Credentials
import json

app = FastAPI(title="PyRoom Web API", description="Web version of PyRoom JANコード management system")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

file_storage = {
    "input.txt": "",
    "checkd01.txt": "",
    "checkd02.txt": "",
    "output.txt": ""
}

SPREADSHEET_ID = "17Le1KA9nzMREt0Qp9_elM1OF1q8aSp-GDBZRPOntNI8"

class JANCodeData(BaseModel):
    jan_code: str
    brand_name: str = "廃番"

class ClipboardData(BaseModel):
    content: str
    jan_code: Optional[str] = ""

class FileContent(BaseModel):
    filename: str
    content: str

class CheckResult(BaseModel):
    duplicates: List[str]
    discontinued_codes: List[str]
    total_count: int
    current_jan_code: Optional[str]
    message: str

def get_google_sheets_client():
    """Initialize Google Sheets client - mock implementation for now"""
    try:
        return None
    except Exception:
        return None

def process_jan_codes(content: str) -> tuple:
    """Extract and process JAN codes from content"""
    jan_codes = re.findall(r'JANコード\t(\d+)', content)
    discontinued_codes = []
    
    for code in jan_codes:
        if f'JANコード\t{code}' in content:
            section = content.split(f'JANコード\t{code}')[1].split('JANコード')[0]
            if 'ブランド名\t廃番' in section:
                discontinued_codes.append(code)
    
    duplicate_jan_codes = [code for code, count in Counter(jan_codes).items() if count > 1]
    
    return jan_codes, discontinued_codes, duplicate_jan_codes

def mock_type1_script():
    """Mock implementation of Type041701a.py functionality"""
    return "サンプルデータ1\nサンプルデータ2\nサンプルデータ3"

def mock_type2_script():
    """Mock implementation of Type2.py functionality"""
    return "出力データ1\n出力データ2\n出力データ3"

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/files/{filename}")
async def get_file(filename: str):
    """Get file content"""
    if filename not in file_storage:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"filename": filename, "content": file_storage[filename]}

@app.post("/api/files/{filename}")
async def upload_file(filename: str, file: UploadFile = File(...)):
    """Upload file content"""
    if filename not in file_storage:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    content = await file.read()
    file_storage[filename] = content.decode('utf-8')
    
    return {"message": f"{filename} uploaded successfully", "filename": filename}

@app.put("/api/files/{filename}")
async def update_file_content(filename: str, file_content: FileContent):
    """Update file content directly"""
    if filename not in file_storage:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_storage[filename] = file_content.content
    return {"message": f"{filename} updated successfully", "filename": filename}

@app.post("/api/process-clipboard")
async def process_clipboard(data: ClipboardData):
    """Process clipboard data and add to input.txt"""
    lines = data.content.split('\n')
    output_data = "\n".join(line.strip() for line in lines if line.strip())
    
    if data.jan_code:
        output_data = f"JANコード\t{data.jan_code}\n{output_data}"
    
    file_storage["input.txt"] += output_data + '\n\n'
    
    return {"message": "新しいデータがinput.txtに追加されました。", "content": output_data}

@app.post("/api/add-discontinued")
async def add_discontinued_jan_code(data: JANCodeData):
    """Add discontinued JAN code to input.txt"""
    content = f"JANコード\t{data.jan_code}\nブランド名\t{data.brand_name}\n\n"
    file_storage["input.txt"] += content
    
    return {"message": "廃番JANコードが追加されました。", "content": content}

@app.get("/api/check-duplicates")
async def check_duplicates():
    """Check for duplicate JAN codes in input.txt"""
    content = file_storage["input.txt"]
    jan_codes, discontinued_codes, duplicate_jan_codes = process_jan_codes(content)
    
    messages = []
    if duplicate_jan_codes:
        for duplicate in duplicate_jan_codes:
            messages.append(f"JANコード {duplicate} が重複しています")
    else:
        messages.append("重複はありません")
    
    for code in discontinued_codes:
        messages.append(f"JANコード {code} は廃番です")
    
    messages.append(f"JANコードは上から{len(jan_codes)}番目です")
    if jan_codes:
        messages.append(f"現在のJANコードは{jan_codes[-1]}です")
    
    return CheckResult(
        duplicates=duplicate_jan_codes,
        discontinued_codes=discontinued_codes,
        total_count=len(jan_codes),
        current_jan_code=jan_codes[-1] if jan_codes else None,
        message="\n".join(messages)
    )

@app.get("/api/check-data-differences")
async def check_data_differences():
    """Check differences between checkd01.txt and checkd02.txt"""
    try:
        lines1 = file_storage["checkd01.txt"].splitlines()
        lines2 = file_storage["checkd02.txt"].splitlines()
        
        differences = []
        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            jan_code1 = re.search(r'\d+', line1)
            jan_code2 = re.search(r'\d+', line2)
            
            if jan_code1 and jan_code2 and jan_code1.group() != jan_code2.group():
                differences.append(f"{i + 1}番目が違います")
        
        if differences:
            message = "\n".join(differences)
        else:
            message = "すべてのJANコードが一致しています"
        
        return {"differences": differences, "message": message}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ抜けチェック中にエラーが発生しました： {str(e)}")

@app.post("/api/run-type1-batch")
async def run_type1_batch():
    """Execute Type1x.bat equivalent functionality"""
    try:
        result = mock_type1_script()
        file_storage["checkd02.txt"] = result
        
        is_empty = not file_storage["checkd01.txt"].strip()
        
        return {
            "message": "Type1x.bat実行完了",
            "output": result,
            "checkd01_empty": is_empty,
            "info_message": "checkd01.txtは空です" if is_empty else "checkd01.txtにデータがあります"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"バッチ実行中にエラーが発生しました： {str(e)}")

@app.post("/api/run-type2-batch")
async def run_type2_batch():
    """Execute Type2x.bat equivalent functionality"""
    try:
        result = mock_type2_script()
        file_storage["output.txt"] = result
        
        return {
            "message": "Type2x.bat実行完了",
            "output": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"バッチ実行中にエラーが発生しました： {str(e)}")

@app.post("/api/clear-files")
async def clear_files():
    """Clear all file contents"""
    for filename in file_storage:
        file_storage[filename] = ""
    
    return {"message": "ファイルのデータをクリアしました。"}

@app.get("/api/check-input-file")
async def check_input_file():
    """Check input.txt for validation issues"""
    try:
        lines = file_storage["input.txt"].splitlines()
        
        invalid_an_code_lines = []
        thirteen_digit_lines = []
        
        for i, line in enumerate(lines, 1):
            if 'ANコード' in line and 'J' not in line:
                invalid_an_code_lines.append(i)
            if re.match(r'^\d{13}$', line.strip()):
                thirteen_digit_lines.append(i)
        
        message = (
            f"「ANコード」に「J」が含まれていない行: {', '.join(map(str, invalid_an_code_lines)) or 'なし'}\n"
            f"13桁の数値のみを含む行: {', '.join(map(str, thirteen_digit_lines)) or 'なし'}"
        )
        
        return {
            "invalid_an_code_lines": invalid_an_code_lines,
            "thirteen_digit_lines": thirteen_digit_lines,
            "message": message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイルのチェック中にエラーが発生しました： {str(e)}")

@app.get("/api/combined-check")
async def combined_check():
    """Combined duplicate and data gap check"""
    try:
        type1_result = await run_type1_batch()
        
        duplicate_result = await check_duplicates()
        
        diff_result = await check_data_differences()
        
        combined_message = duplicate_result.message + "\n\nJANコードのチェック結果：\n" + diff_result["message"]
        
        return {
            "duplicate_check": duplicate_result,
            "data_differences": diff_result,
            "type1_result": type1_result,
            "combined_message": combined_message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"統合チェック中にエラーが発生しました： {str(e)}")

@app.get("/api/google-sheets/jan-codes")
async def get_google_sheets_jan_codes():
    """Get JAN codes from Google Sheets"""
    try:
        client = get_google_sheets_client()
        if not client:
            return {"message": "Google Sheets接続が利用できません（認証情報が必要）", "codes": []}
        
        mock_codes = ["4977292361613", "4977292361614", "4977292361615"]
        
        return {"codes": mock_codes, "message": "Google SheetsからJANコードを取得しました"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Sheets取得中にエラーが発生しました： {str(e)}")

@app.get("/api/status")
async def get_status():
    """Get application status and file information"""
    file_info = {}
    for filename, content in file_storage.items():
        file_info[filename] = {
            "size": len(content),
            "lines": len(content.splitlines()) if content else 0,
            "empty": not content.strip()
        }
    
    return {
        "status": "running",
        "files": file_info,
        "google_sheets_available": get_google_sheets_client() is not None
    }
