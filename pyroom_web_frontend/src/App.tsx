import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Upload, Download, FileText, CheckCircle, AlertCircle } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface FileInfo {
  size: number;
  lines: number;
  empty: boolean;
}

interface AppStatus {
  status: string;
  files: Record<string, FileInfo>;
  google_sheets_available: boolean;
}

function App() {
  const [output, setOutput] = useState<string>('');
  const [loading, setLoading] = useState<string>('');
  const [status, setStatus] = useState<AppStatus | null>(null);
  const [clipboardContent, setClipboardContent] = useState<string>('');
  const [janCode, setJanCode] = useState<string>('');
  const [discontinuedJanCode, setDiscontinuedJanCode] = useState<string>('');
  const [showDiscontinuedDialog, setShowDiscontinuedDialog] = useState<boolean>(false);
  const [showClipboardDialog, setShowClipboardDialog] = useState<boolean>(false);

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`);
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Status fetch error:', error);
    }
  };

  const apiCall = async (endpoint: string, method: string = 'GET', body?: any) => {
    setLoading(endpoint);
    try {
      const options: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };
      
      if (body) {
        options.body = JSON.stringify(body);
      }

      const response = await fetch(`${API_URL}${endpoint}`, options);
      const data = await response.json();
      
      if (data.message) {
        setOutput(prev => prev + '\n' + data.message);
      }
      
      if (data.combined_message) {
        setOutput(data.combined_message);
      }
      
      await fetchStatus();
      return data;
    } catch (error) {
      setOutput(prev => prev + '\nエラー: ' + error);
    } finally {
      setLoading('');
    }
  };

  const downloadFile = async (filename: string) => {
    try {
      const response = await fetch(`${API_URL}/api/files/${filename}`);
      const data = await response.json();
      
      const blob = new Blob([data.content], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      setOutput(prev => prev + '\nダウンロードエラー: ' + error);
    }
  };

  const uploadFile = async (filename: string, content: string) => {
    await apiCall(`/api/files/${filename}`, 'PUT', { filename, content });
  };

  const handleFileUpload = (filename: string) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt';
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const content = await file.text();
        await uploadFile(filename, content);
      }
    };
    input.click();
  };

  const handleClipboardProcess = async () => {
    await apiCall('/api/process-clipboard', 'POST', {
      content: clipboardContent,
      jan_code: janCode
    });
    setClipboardContent('');
    setJanCode('');
    setShowClipboardDialog(false);
  };

  const handleDiscontinuedAdd = async () => {
    await apiCall('/api/add-discontinued', 'POST', {
      jan_code: discontinuedJanCode,
      brand_name: '廃番'
    });
    setDiscontinuedJanCode('');
    setShowDiscontinuedDialog(false);
  };

  const buttons = [
    {
      text: '重複と項目抜けのチェック',
      action: () => apiCall('/api/combined-check'),
      color: 'bg-green-600 hover:bg-green-700',
      row: 1, col: 0
    },
    {
      text: 'JANコード等のコピー',
      action: () => setOutput('この機能は現在工事中です。\nしばらくお待ちください。'),
      color: 'bg-red-600 hover:bg-red-700',
      row: 1, col: 1
    },
    {
      text: 'テキストに貼り付けと実行',
      action: () => setShowClipboardDialog(true),
      color: 'bg-green-600 hover:bg-green-700',
      row: 2, col: 1
    },
    {
      text: 'データ抜けのチェック',
      action: () => apiCall('/api/run-type1-batch', 'POST'),
      color: 'bg-red-600 hover:bg-red-700',
      row: 2, col: 2
    },
    {
      text: 'チェックシートを開く',
      action: () => setOutput('この機能は現在工事中です。\nしばらくお待ちください。'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 3, col: 0
    },
    {
      text: '座標軸とコピー',
      action: () => setOutput('この機能は現在工事中です。\nしばらくお待ちください。'),
      color: 'bg-red-600 hover:bg-red-700',
      row: 2, col: 0
    },
    {
      text: '商品情報入力シートを開く',
      action: () => setOutput('この機能は現在工事中です。\nしばらくお待ちください。'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 3, col: 1
    },
    {
      text: '藤原産業を開く',
      action: () => setOutput('この機能は現在工事中です。\nしばらくお待ちください。'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 3, col: 2
    },
    {
      text: 'input.txtのチェック',
      action: () => apiCall('/api/check-input-file'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 4, col: 0
    },
    {
      text: 'サブフォーム廃番処理',
      action: () => setShowDiscontinuedDialog(true),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 4, col: 1
    },
    {
      text: 'Type2x.bat実行とoutput.txt表示',
      action: () => apiCall('/api/run-type2-batch', 'POST'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 4, col: 2
    },
    {
      text: 'checkd01.txtを開く',
      action: () => downloadFile('checkd01.txt'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 5, col: 1
    },
    {
      text: 'checkd02.txtを開く',
      action: () => downloadFile('checkd02.txt'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 5, col: 2
    },
    {
      text: 'クリップボードのクリア',
      action: () => apiCall('/api/clear-files', 'POST'),
      color: 'bg-blue-600 hover:bg-blue-700',
      row: 5, col: 0
    },
    {
      text: 'input.txtを開く',
      action: () => downloadFile('input.txt'),
      color: 'bg-red-600 hover:bg-red-700',
      row: 1, col: 2
    }
  ];

  const gridButtons = Array.from({ length: 6 }, () => Array(3).fill(null));
  buttons.forEach(button => {
    gridButtons[button.row][button.col] = button;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">
              JANコード管理システム
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              value={output}
              onChange={(e) => setOutput(e.target.value)}
              className="w-full h-48 mb-4 font-mono text-sm"
              placeholder="処理結果がここに表示されます..."
            />
            
            <div className="grid grid-cols-3 gap-2 mb-4">
              {gridButtons.map((row, rowIndex) =>
                row.map((button, colIndex) => (
                  <div key={`${rowIndex}-${colIndex}`} className="h-12">
                    {button ? (
                      <Button
                        onClick={button.action}
                        disabled={loading !== ''}
                        className={`w-full h-full text-xs ${button.color} text-white`}
                      >
                        {loading === button.text ? '処理中...' : button.text}
                      </Button>
                    ) : (
                      <div className="w-full h-full"></div>
                    )}
                  </div>
                ))
              )}
            </div>

            <div className="space-y-2 text-red-600 font-bold text-lg">
              <p>※商品情報入力シートに必ず名前を明示すること</p>
              <p>※チェックシートの内容をcheckd01.txtにコピーする</p>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                ファイル管理
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {['input.txt', 'checkd01.txt', 'checkd02.txt', 'output.txt'].map(filename => (
                  <div key={filename} className="flex items-center justify-between p-2 border rounded">
                    <span className="font-mono text-sm">{filename}</span>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleFileUpload(filename)}
                      >
                        <Upload className="w-4 h-4 mr-1" />
                        アップロード
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => downloadFile(filename)}
                      >
                        <Download className="w-4 h-4 mr-1" />
                        ダウンロード
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5" />
                システム状態
              </CardTitle>
            </CardHeader>
            <CardContent>
              {status && (
                <div className="space-y-2">
                  <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      ステータス: {status.status}
                    </AlertDescription>
                  </Alert>
                  <div className="text-sm">
                    <p>Google Sheets: {status.google_sheets_available ? '利用可能' : '認証情報が必要'}</p>
                    <p>ファイル数: {Object.keys(status.files).length}</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Dialog open={showClipboardDialog} onOpenChange={setShowClipboardDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>クリップボードデータの処理</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">JANコード (オプション)</label>
                <Input
                  value={janCode}
                  onChange={(e) => setJanCode(e.target.value)}
                  placeholder="JANコードを入力..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">クリップボードの内容</label>
                <Textarea
                  value={clipboardContent}
                  onChange={(e) => setClipboardContent(e.target.value)}
                  placeholder="貼り付けるデータを入力..."
                  rows={6}
                />
              </div>
              <Button onClick={handleClipboardProcess} className="w-full">
                処理実行
              </Button>
            </div>
          </DialogContent>
        </Dialog>

        <Dialog open={showDiscontinuedDialog} onOpenChange={setShowDiscontinuedDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>廃番JANコード入力</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">JANコード</label>
                <Input
                  value={discontinuedJanCode}
                  onChange={(e) => setDiscontinuedJanCode(e.target.value)}
                  placeholder="廃番JANコードを入力..."
                />
              </div>
              <Button onClick={handleDiscontinuedAdd} className="w-full">
                廃番として追加
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}

export default App;
