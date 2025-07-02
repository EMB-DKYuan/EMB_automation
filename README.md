EMB Automation - 自動化測試專案
本專案是一個基於 Pytest 和 SeleniumBase 的自動化測試框架，旨在提供一個整合了 UI 測試與 API 測試的解決方案。它支援並行測試、失敗重試，並透過 Testmo CLI 整合測試報告上傳功能。

目錄
專案特色

專案結構

開始使用

環境需求

安裝步驟

如何執行測試

基本執行

進階選項

測試報告

如何貢獻

疑難排解

專案特色
整合測試：同時支援 UI 和 API 自動化測試。

主流框架：使用業界廣泛採用的 Pytest 與 SeleniumBase。

高效執行：支援多種執行模式，包括並行測試、無頭模式與失敗重試。

報告整合：可生成本地 HTML 測試報告，並透過 Testmo CLI 上傳結果至測試管理平台。

專案結構
專案的主要目錄和檔案結構如下：

text
EMB_automation/
├── .env                    # 環境變數配置 (需從 .env.example 複製建立)
├── .env.example            # 環境變數範本
├── .gitignore              # Git 忽略檔案清單
├── conftest.py             # Pytest 共用配置 (例如 Fixtures)
├── pytest.ini              # Pytest 主要設定檔
├── requirements.txt        # Python 依賴套件清單
├── run_test.py             # 主執行腳本 (可選)
├── reports/                # 測試報告輸出目錄
└── tests/                  # 測試腳本主目錄
    ├── api/                # API 測試案例
    └── ui/                 # UI 測試案例
開始使用
環境需求
在開始之前，請確保您的開發環境已安裝以下軟體：

Python: 3.9 或以上版本

Node.js: 16 或以上版本 (用於 Testmo CLI)

Git: 最新版本

安裝步驟
Clone 專案

bash
git clone https://github.com/EMB-DKYuan/EMB_automation.git
cd EMB_automation
設定環境變數
從範本檔案複製一份 .env 設定檔，並根據您的環境填寫必要的變數（如帳號、密碼、API 位址等）。

bash
cp .env.example .env
安裝 Python 依賴
建議升級 pip 並安裝 requirements.txt 中的所有套件。

bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
安裝瀏覽器驅動
此專案使用 SeleniumBase 管理瀏覽器驅動。推薦安裝 Chrome 驅動。

bash
python3 -m seleniumbase install chromedriver
您也可以安裝其他瀏覽器驅動：

bash
# 安裝 Firefox 驅動
python3 -m seleniumbase install geckodriver
# 安裝 Edge 驅動
python3 -m seleniumbase install edgedriver
安裝 Testmo CLI (選用)
如果您需要將測試報告上傳至 Testmo，請安裝其命令列工具。

bash
npm install -g @testmo/testmo-cli
驗證安裝是否成功：

bash
testmo --version
如何執行測試
基本執行
執行所有測試
此指令會執行 tests/ 目錄下的所有測試，並生成一份獨立的 HTML 報告。

bash
python3 -m pytest tests/ --html=reports/report.html --self-contained-html -v
執行特定類型的測試
您可以單獨執行 UI 或 API 測試。

bash
# 僅執行 UI 測試
python3 -m pytest tests/ui/ -v

# 僅執行 API 測試
python3 -m pytest tests/api/ -v
執行單一測試檔案
若要針對特定檔案進行測試，請指定其路徑。

bash
python3 -m pytest tests/ui/test_ui_登入登出_kbb.py -v
進階選項
並行執行 (Parallel Execution)
使用 -n 參數可自動分配核心數來加速測試。

bash
python3 -m pytest tests/ -n auto --html=reports/parallel_report.html
無頭模式 (Headless Mode)
在背景執行 UI 測試，不會開啟瀏覽器視窗。

bash
python3 -m pytest tests/ --headless --html=reports/headless_report.html
失敗重試 (Reruns)
當測試失敗時，自動重試指定的次數。

bash
python3 -m pytest tests/ --reruns 3 --html=reports/retry_report.html
測試報告
執行測試後，HTML 報告會儲存在 reports/ 目錄下。您可以使用瀏覽器打開檔案來查看詳細結果。

bash
# macOS 範例
open reports/report.html
如何貢獻
歡迎為此專案新增測試案例。請遵循以下規則：

API 測試: 在 tests/api/ 目錄下建立 test_*.py 格式的檔案。

UI 測試: 在 tests/ui/ 目錄下建立 test_*.py 格式的檔案。

疑難排解
如果您遇到問題，可以嘗試以下步驟進行檢查：

確認 pytest 執行方式：請務必使用 python3 -m pytest 而非 pytest，以確保使用的是當前專案環境的套件。

更新瀏覽器驅動：若瀏覽器已更新，請重新執行安裝指令來更新驅動。

bash
python3 -m seleniumbase install chromedriver --upgrade
檢查目錄權限：確保 reports/ 目錄具有寫入權限。

bash
chmod 755 reports/
版本檢查：確認各工具版本是否符合要求。

bash
# 檢查 Python 版本
python3 --version
# 檢查 SeleniumBase 版本
python3 -m seleniumbase --version
# 檢查 Testmo CLI 版本
testmo --version