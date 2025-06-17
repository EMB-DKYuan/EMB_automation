環境需求
Python: 3.9 或以上版本

Node.js: 16 或以上版本（用於 Testmo CLI）

Git: 最新版本

作業系統: macOS, Linux, Windows

# 升級 pip
python3 -m pip install --upgrade pip

# 安裝專案依賴
pip install -r requirements.txt

# 安裝 Chrome 驅動（推薦）
python3 -m seleniumbase install chromedriver

# 可選：安裝其他瀏覽器驅動
python3 -m seleniumbase install geckodriver  # Firefox
python3 -m seleniumbase install edgedriver   # Edge

# 安裝 Testmo CLI（用於報告上傳）
npm install -g @testmo/testmo-cli

# 驗證安裝
testmo --version

CBO_KBB/
├── .env                    # 環境變數配置
├── .env.example           # 環境變數範本
├── .gitignore             # Git 忽略檔案
├── conftest.py            # pytest 共用配置
├── pytest.ini            # pytest 設定檔
├── requirements.txt       # Python 依賴清單
├── run_test.py           # 主執行腳本
├── README.md             # 專案說明文件
├── libs/                 # 共用函式庫（已棄用）
├── reports/              # 測試報告輸出目錄
└── tests/                # 測試腳本目錄
    ├── api/              # API 測試
    │   └── test_api_登入登出_kbb.py
    └── ui/               # UI 測試
        ├── test_ui_登入登出_kbb.py
        └── test_ui_密碼修改失敗_kbb.py

# 執行所有測試
python3 -m pytest tests/ --html=reports/report.html --self-contained-html -v

# 執行特定測試
python3 -m pytest tests/ui/test_ui_登入登出_kbb.py -v

# 執行 API 測試
python3 -m pytest tests/api/ -v

# 執行 UI 測試
python3 -m pytest tests/ui/ -v

# 並行執行測試
python3 -m pytest tests/ -n auto --html=reports/parallel_report.html

# 失敗重試
python3 -m pytest tests/ --reruns 3 --html=reports/retry_report.html

# 無頭模式執行
python3 -m pytest tests/ --headless --html=reports/headless_report.html

# 在瀏覽器中打開報告
open reports/report_YYYYMMDD_HHMMSS.html

# 確保使用 python3 -m pytest 而非直接使用 pytest
python3 -m pytest --version

# 重新安裝瀏覽器驅動
python3 -m seleniumbase install chromedriver --upgrade

# 確保報告目錄有寫入權限
chmod 755 reports/

# 檢查 Python 版本
python3 --version

# 檢查 SeleniumBase 安裝
python3 -m seleniumbase --version

# 檢查 pytest 插件
python3 -m pytest --trace-config | grep seleniumbase

# 檢查 Testmo CLI
testmo --version

新增測試案例
API 測試：在 tests/api/ 目錄下建立 test_*.py 檔案

UI 測試：在 tests/ui/ 目錄下建立 test_*.py 檔案