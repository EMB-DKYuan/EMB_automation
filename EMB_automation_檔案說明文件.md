# EMB_automation 專案檔案說明文件

## 目錄
- [專案概述](#專案概述)
- [快速入門指南](#快速入門指南)
- [配置檔案說明](#配置檔案說明)
- [工具庫檔案說明](#工具庫檔案說明)
- [執行檔案說明](#執行檔案說明)
- [測試檔案說明](#測試檔案說明)
- [使用說明](#使用說明)
- [維護指南](#維護指南)
- [故障排除](#故障排除)

---

## 專案概述

EMB_automation 是一個基於 SeleniumBase 和 pytest 的自動化測試框架，支援多平台（CBO、KBB、CC）的 UI 和 API 測試。專案採用模組化設計，提供統一的配置管理、測試執行和報告生成功能。

### 主要特色
- **多平台支援**：支援 CBO、KBB、CC 等多個平台
- **多環境配置**：支援 UAT、STG 等不同環境
- **雙重測試**：同時支援 UI 和 API 測試
- **自動化報告**：整合 HTML 報告和 Testmo 平台
- **郵件通知**：測試失敗時自動發送通知
- **靈活配置**：支援 YAML 配置和環境變數

---

## 快速入門指南

### 1. 環境設置

#### 安裝依賴
```bash
pip install -r requirements.txt
```

#### 安裝 Testmo CLI（可選）
```bash
sudo npm install -g @testmo/testmo-cli
```

### 2. 配置設定

#### 複製並編輯環境變數檔案
```bash
cp .env.example .env
```

#### 必要配置項目
- `ENVIRONMENT`: 設定執行環境（stg/uat）
- `TEST_MODE`: 設定測試模式（cbo/kbb/cc/all）
- 各平台的登入憑證和 URL

### 3. 執行測試

#### 基本執行
```bash
python run_test.py
```

#### 指定測試模式
```bash
TEST_MODE=cbo python run_test.py
```

#### 指定環境
```bash
ENVIRONMENT=uat python run_test.py
```

### 4. 查看報告

測試完成後，報告將生成在 `reports/` 目錄下：
- HTML 報告：`reports/report_YYYYMMDD_HHMMSS.html`
- XML 報告：`reports/results_YYYYMMDD_HHMMSS.xml`
- Testmo 平台：自動上傳（如已配置）

---

## 配置檔案說明

### 1. `.env` - 環境變數配置

**檔案用途**：
- 儲存敏感資訊（帳號密碼、API 金鑰）
- 控制測試執行環境和模式
- 配置第三方服務（Testmo、郵件）

**主要配置區塊**：

#### Testmo 設定
```env
TESTMO_EMAIL=your-email@example.com          # Testmo 登入郵箱
TESTMO_EMAIL_PW=your-app-password            # Gmail 應用程式密碼
TESTMO_RECEIVERS=receiver@example.com        # 通知接收者
TESTMO_INSTANCE=https://your.testmo.net      # Testmo 實例 URL
TESTMO_PROJECT_ID=7                          # 專案 ID
UPLOAD_TESTMO=true                           # 是否上傳到 Testmo
```

#### 環境控制
```env
ENVIRONMENT=stg                              # 執行環境（stg/uat）
BROWSER=chrome                               # 瀏覽器類型
HEADLESS=true                                # 是否無頭模式
TEST_MODE=cbo                                # 測試模式
```

#### 測試帳號設定
```env
CBO_USER_ID=your_cbo_user                    # CBO 一般使用者帳號
CBO_PASSWORD=your_password                   # CBO 一般使用者密碼
CBO_ADMIN_USER_ID=admin_user                 # CBO 管理員帳號
CBO_ADMIN_PASSWORD=admin_password            # CBO 管理員密碼
```

#### 平台 URL 配置
```env
CBO_LOGIN_URL_UAT=https://uat-url.com        # CBO UAT 環境 URL
CBO_LOGIN_URL_STG=https://stg-url.com        # CBO STG 環境 URL
CBO_API_URL_UAT=https://api-uat-url.com      # CBO UAT API URL
CBO_API_URL_STG=https://api-stg-url.com      # CBO STG API URL
```

**使用注意事項**：
- 不要將 `.env` 檔案提交到版本控制系統
- 密碼應使用強密碼並定期更換
- Gmail 需要使用應用程式密碼而非一般密碼

### 2. [`config.py`](config.py:1) - 核心配置類

**檔案用途**：
- 提供統一的配置管理介面
- 實現環境相關的動態配置
- 封裝 URL 生成邏輯

**主要類別和方法**：

#### [`TestConfig`](config.py:6) 類別
```python
class TestConfig:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "uat").upper()
```

**核心方法**：

##### [`_get_env_specific_value()`](config.py:12)
```python
@classmethod
def _get_env_specific_value(cls, base_var_name):
    """根據當前環境動態獲取配置值"""
```
- **功能**：根據環境變數動態獲取對應的配置值
- **範例**：`ENVIRONMENT="STG"` 時，`CBO_LOGIN_URL` 會取得 `CBO_LOGIN_URL_STG`

##### [`build_ui_url()`](config.py:77)
```python
@classmethod
def build_ui_url(cls, path_key="login", domain_name="KBB"):
    """根據 domain_name 獲取對應的 UI 登入 URL"""
```
- **參數**：
  - `path_key`: URL 路徑類型（目前僅支援 "login"）
  - `domain_name`: 平台名稱（CBO/KBB/CCCOMPANY/CCAGENT）
- **回傳**：完整的登入 URL

##### [`build_api_url()`](config.py:96)
```python
@classmethod
def build_api_url(cls, path_key="login", domain_name="KBB"):
    """動態生成完整的 API URL"""
```
- **參數**：
  - `path_key`: API 路徑類型（login/logout/password）
  - `domain_name`: 平台名稱
- **回傳**：完整的 API URL

**使用範例**：
```python
from config import TestConfig

# 獲取 CBO 登入 URL
login_url = TestConfig.build_ui_url("login", "CBO")

# 獲取 API URL
api_url = TestConfig.build_api_url("login", "CBO")

# 直接存取配置
user_id = TestConfig.CBO_USER_ID
```

### 3. [`test_path_config.yaml`](test_path_config.yaml:1) - 測試路徑配置

**檔案用途**：
- 定義不同測試模式的執行路徑
- 支援測試案例的分類管理
- 提供靈活的測試執行控制

**配置結構**：

#### 測試路徑分類
```yaml
test_paths:
  unit_tests:                                # 單元測試
    - tests/CC/company/ui/test_ui_Login&out_cc.py
  
  ui_tests:                                  # UI 測試
    - tests/CBO/ui/test_ui_Login&out_cbo.py
    - tests/CBO_KBB/ui/test_ui_登入登出_kbb.py
  
  api_tests:                                 # API 測試
    - tests/CBO/api/test_api_登入登出_cbo.py
    - tests/CBO_KBB/api/test_api_登入登出_kbb.py
  
  cbo_tests:                                 # CBO 平台測試
    - tests/CBO/api/test_api_登入登出_cbo.py
    - tests/CBO/ui/test_ui_Login&out_cbo.py
  
  kbb_tests:                                 # KBB 平台測試
    - tests/CBO_KBB/api/test_api_登入登出_kbb.py
    - tests/CBO_KBB/ui/test_ui_登入登出_kbb.py
```

#### 執行模式
```yaml
mode: all, unit, ui, api, kbb, cbo
```

**使用方式**：
```bash
# 執行所有測試
TEST_MODE=all python run_test.py

# 執行 CBO 平台測試
TEST_MODE=cbo python run_test.py

# 執行 UI 測試
TEST_MODE=ui python run_test.py
```

### 4. [`pytest.ini`](pytest.ini:1) - Pytest 配置

**檔案用途**：
- 配置 pytest 的預設行為
- 設定測試報告格式
- 定義測試路徑

**配置內容**：
```ini
[pytest]
addopts = 
    --html=reports/report.html               # HTML 報告路徑
    --self-contained-html                    # 自包含 HTML
testpaths = tests                            # 測試路徑
```

### 5. [`requirements.txt`](requirements.txt:1) - 依賴管理

**檔案用途**：
- 定義專案所需的 Python 套件
- 確保環境一致性

**主要依賴**：
```txt
pytest                                       # 測試框架
pytest-html                                 # HTML 報告生成
selenium                                    # Web 自動化
requests                                    # HTTP 請求
pyyaml                                      # YAML 解析
seleniumbase==4.38.0                       # SeleniumBase 框架
```

---

## 工具庫檔案說明

### 1. [`libs/ui_custom_base.py`](libs/ui_custom_base.py:1) - UI 自訂基礎類

**檔案用途**：
- 擴展 SeleniumBase 功能
- 提供通用的 UI 操作方法
- 實現平台特定的操作封裝

**主要類別**：

#### [`CustomBase`](libs/ui_custom_base.py:11) 類別
繼承自 `BaseCase`，提供增強的 UI 測試功能。

**核心方法分類**：

##### 視窗和顯示控制
```python
def specific_window_size_max(self):          # 最大化視窗
def specific_window_size(self, width=1920, height=1080):  # 設定視窗大小
def set_page_zoom(self, level=100):          # 設定頁面縮放
def set_browser_zoom(self, level=100):       # 設定瀏覽器縮放
```

##### 截圖功能
```python
def save_screenshot_with_full_path(self, task_name=None):
```
- **功能**：儲存截圖到結構化路徑
- **路徑結構**：`reports/執行時間戳/測試模式/腳本名稱/`
- **檔名格式**：`HHMMSS_fff_任務名稱.png`

##### 平台配置管理
```python
def _get_platform_config(self, platform):
```
- **功能**：獲取指定平台的 UI 元素和帳密配置
- **支援平台**：CBO、KBB、CCCOMPANY、CCAGENT
- **回傳內容**：使用者憑證、UI 選擇器、佔位符文字

##### 通用登入登出
```python
def login(self, platform, user_id=None, password=None, is_admin=False):
def logout(self, platform):
def login_page_check(self, platform):
```

**使用範例**：
```python
from libs.ui_custom_base import CustomBase

class TestExample(CustomBase):
    def test_login(self):
        self.specific_window_size()          # 設定視窗大小
        self.open("https://example.com")
        self.login("CBO")                    # 使用預設帳密登入
        self.save_screenshot_with_full_path("登入成功")
        self.logout("CBO")
```

##### CBO 平台特定方法
```python
def type_wrong_user_id_cbo(self):           # 輸入錯誤使用者 ID
def type_wrong_password_cbo(self):          # 輸入錯誤密碼
def click_resetpassword_cbo(self):          # 點擊重設密碼
def type_duplicated_password_cbo(self):     # 輸入重複密碼
def admin_reset_password_dkyuan_all_cbo(self): # 管理員重設密碼
```

##### KBB 平台特定方法
```python
def click_resetpassword_kbb(self):          # KBB 重設密碼
def type_duplicated_password_kbb(self):     # KBB 輸入重複密碼
```

### 2. [`libs/api_client.py`](libs/api_client.py:1) - API 客戶端

**檔案用途**：
- 封裝 HTTP 請求操作
- 提供統一的 API 呼叫介面
- 支援 URL 自動拼接

**主要類別**：

#### [`APIClient`](libs/api_client.py:3) 類別
```python
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
```

**核心方法**：

##### [`request()`](libs/api_client.py:25)
```python
def request(self, method, url, **kwargs):
```
- **參數**：
  - `method`: HTTP 方法（GET/POST/PUT/DELETE）
  - `url`: 請求 URL（支援相對路徑和絕對路徑）
  - `**kwargs`: 其他請求參數（headers、params、json、data 等）
- **功能**：自動處理 URL 拼接，發送 HTTP 請求
- **回傳**：`requests.Response` 物件

**使用範例**：
```python
from libs.api_client import APIClient

# 初始化客戶端
client = APIClient("https://api.example.com")

# GET 請求
response = client.request("GET", "/users", params={"page": 1})

# POST 請求
response = client.request("POST", "/users", 
                         json={"name": "John"},
                         headers={"Authorization": "Bearer token"})

# 使用絕對 URL
response = client.request("GET", "https://external-api.com/data")
```

**擴展建議**：
可以新增便利方法來簡化常用操作：
```python
def get(self, url, **kwargs):
    return self.request("GET", url, **kwargs)

def post(self, url, **kwargs):
    return self.request("POST", url, **kwargs)
```

---

## 執行檔案說明

### [`run_test.py`](run_test.py:1) - 測試執行腳本

**檔案用途**：
- 統一的測試執行入口
- 整合測試報告生成
- 提供 Testmo 上傳和郵件通知功能

**主要功能模組**：

#### 1. 測試路徑管理
```python
def get_test_paths():
```
- **功能**：從 YAML 配置檔案獲取測試路徑
- **支援模式**：all、unit、ui、api、kbb、cbo
- **回退機制**：YAML 不存在時使用環境變數

#### 2. pytest 命令建構
```python
def build_pytest_cmd(html_report, xml_report):
```
- **功能**：建構純粹的 pytest 執行命令
- **參數**：
  - `-v`: 詳細輸出
  - `--capture=no`: 不捕獲輸出
  - `-rP`: 顯示通過的測試
  - `--html`: HTML 報告路徑
  - `--junitxml`: XML 報告路徑

#### 3. Testmo 整合
```python
def upload_to_testmo(xml_report, timestamp):
```
- **功能**：獨立的 Testmo 上傳功能
- **命令**：使用 `testmo automation:run:submit`
- **回傳**：Testmo 報告 URL 或錯誤訊息
- **超時控制**：120 秒超時保護

#### 4. 主執行流程
```python
def main():
```
**執行階段**：
1. **測試執行**：執行 SeleniumBase 測試
2. **報告上傳**：上傳結果到 Testmo
3. **郵件通知**：測試失敗時發送通知

**報告生成**：
- HTML 報告：`reports/report_YYYYMMDD_HHMMSS.html`
- XML 報告：`reports/results_YYYYMMDD_HHMMSS.xml`

**使用方式**：
```bash
# 基本執行
python run_test.py

# 指定環境變數
TEST_MODE=cbo ENVIRONMENT=uat python run_test.py

# 禁用 Testmo 上傳
UPLOAD_TESTMO=false python run_test.py
```

**環境變數控制**：
- `TEST_MODE`: 測試模式（從 YAML 配置讀取）
- `UPLOAD_TESTMO`: 是否上傳到 Testmo
- `TESTMO_*`: Testmo 相關配置
- `TESTMO_EMAIL*`: 郵件通知配置

---

## 測試檔案說明

### 測試檔案結構

```
tests/
├── CBO/                    # CBO 平台測試
│   ├── api/               # API 測試
│   └── ui/                # UI 測試
├── CBO_KBB/               # KBB 平台測試
│   ├── api/
│   └── ui/
└── CC/                    # CC 平台測試
    ├── agent/
    └── company/
        ├── api/
        └── ui/
```

### UI 測試檔案範例

#### [`tests/CBO/ui/test_ui_Login&out_cbo.py`](tests/CBO/ui/test_ui_Login&out_cbo.py:1)

**檔案用途**：
- CBO 平台的 UI 登入登出測試
- 驗證登入頁面元素和登入流程

**測試類別**：
```python
class TestUI登入登出CBO(CustomBase):
```

**測試方法**：
```python
def test_ui_login_logout(self):
```

**測試流程**：
1. **視窗設定**：設定瀏覽器視窗大小
2. **頁面開啟**：開啟登入頁面
3. **頁面驗證**：檢查登入頁面元素
4. **執行登入**：使用預設憑證登入
5. **登入驗證**：確認登入成功
6. **執行登出**：登出系統
7. **登出驗證**：確認回到登入頁面

**截圖記錄**：
- 每個關鍵步驟都會自動截圖
- 截圖儲存到結構化路徑

### API 測試檔案範例

#### [`tests/CBO/api/test_api_登入登出_cbo.py`](tests/CBO/api/test_api_登入登出_cbo.py:1)

**檔案用途**：
- CBO 平台的 API 登入登出測試
- 驗證 API 回應格式和業務邏輯

**測試類別**：
```python
class TestAPI_登入登出_CBO(BaseCase):
```

**測試方法**：

##### [`test_api_login()`](tests/CBO/api/test_api_登入登出_cbo.py:8)
**測試流程**：
1. **URL 建構**：使用 `TestConfig.build_api_url()` 建構登入 URL
2. **請求準備**：準備登入 payload 和 headers
3. **發送請求**：使用 `requests.post()` 發送登入請求
4. **狀態驗證**：驗證 HTTP 狀態碼為 200
5. **資料提取**：提取 token、userId、role 等資訊
6. **業務驗證**：驗證業務狀態碼和回應訊息

**請求格式**：
```python
payload = {
    "userId": TestConfig.CBO_USER_ID,
    "password": TestConfig.CBO_PASSWORD,
    "platformCode": TestConfig.CBO_PLATFORM_CODE
}
```

##### [`test_api_logout()`](tests/CBO/api/test_api_登入登出_cbo.py:58)
**測試流程**：
1. **前置檢查**：確保已有登入 token
2. **URL 建構**：建構登出 API URL
3. **標頭準備**：包含 Authorization 和 Uid 標頭
4. **發送請求**：發送登出請求
5. **結果驗證**：驗證登出成功

### 其他測試類型

#### 密碼相關測試
- `test_ui_PasswordChangFail_cbo.py`: 密碼修改失敗測試
- `test_ui_WrongPasswordLogin_cbo.py`: 錯誤密碼登入測試
- `test_ui_AdminResetrUserPassword_cbo.py`: 管理員重設使用者密碼

#### 頁面功能測試
- `test_ui_AllPageCheck_cbo.py`: 全頁面點擊測試

#### 平台特定測試
- KBB 平台：`tests/CBO_KBB/` 目錄下的測試
- CC 平台：`tests/CC/` 目錄下的測試

---

## 使用說明

### 1. 基本使用流程

#### 步驟 1：環境準備
```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 配置環境變數
cp .env.example .env
# 編輯 .env 檔案，設定必要的配置

# 3. 驗證配置
python -c "from config import TestConfig; print(TestConfig.CBO_LOGIN_URL())"
```

#### 步驟 2：執行測試
```bash
# 執行所有測試
python run_test.py

# 執行特定平台測試
TEST_MODE=cbo python run_test.py

# 執行特定類型測試
TEST_MODE=ui python run_test.py

# 指定環境執行
ENVIRONMENT=uat TEST_MODE=cbo python run_test.py
```

#### 步驟 3：查看結果
```bash
# 查看 HTML 報告
open reports/report_YYYYMMDD_HHMMSS.html

# 查看 XML 報告
cat reports/results_YYYYMMDD_HHMMSS.xml

# 查看 Testmo 報告（如已配置）
# 會在執行完成後顯示 URL
```

### 2. 常見使用場景

#### 場景 1：日常回歸測試
```bash
# 執行所有平台的核心功能測試
TEST_MODE=all ENVIRONMENT=uat python run_test.py
```

#### 場景 2：新功能驗證
```bash
# 只執行 UI 測試驗證介面功能
TEST_MODE=ui ENVIRONMENT=stg python run_test.py
```

#### 場景 3：API 介面測試
```bash
# 只執行 API 測試驗證後端功能
TEST_MODE=api ENVIRONMENT=stg python run_test.py
```

#### 場景 4：特定平台測試
```bash
# 只測試 CBO 平台
TEST_MODE=cbo ENVIRONMENT=uat python run_test.py
```

#### 場景 5：本地開發測試
```bash
# 關閉 Testmo 上傳，加快執行速度
UPLOAD_TESTMO=false TEST_MODE=cbo python run_test.py
```

### 3. 進階使用技巧

#### 自訂測試路徑
編輯 `test_path_config.yaml`：
```yaml
test_paths:
  custom_tests:
    - tests/CBO/ui/test_ui_Login&out_cbo.py
    - tests/CBO/api/test_api_登入登出_cbo.py
```

然後執行：
```bash
TEST_MODE=custom python run_test.py
```

#### 使用 pytest 直接執行
```bash
# 執行特定測試檔案
pytest tests/CBO/ui/test_ui_Login&out_cbo.py -v

# 執行特定測試方法
pytest tests/CBO/ui/test_ui_Login&out_cbo.py::TestUI登入登出CBO::test_ui_login_logout -v

# 使用標記執行
pytest -m "smoke" -v
```

#### 並行執行（需安裝 pytest-xdist）
```bash
pip install pytest-xdist
pytest -n 4 tests/ -v  # 使用 4 個並行程序
```

### 4. 報告和監控

#### HTML 報告功能
- **測試結果概覽**：通過/失敗統計
- **詳細日誌**：每個測試的執行日誌
- **截圖記錄**：失敗時的頁面截圖
- **執行時間**：每個測試的執行時間

#### Testmo 整合
- **自動上傳**：測試完成後自動上傳結果
- **歷史追蹤**：可查看歷史執行記錄
- **團隊協作**：團隊成員可共享測試結果

#### 郵件通知
- **失敗通知**：測試失敗時自動發送郵件
- **報告連結**：郵件包含 Testmo 和本地報告連結
- **錯誤摘要**：包含錯誤訊息摘要

---

## 維護指南

### 1. 新增測試案例

#### 新增 UI 測試
1. **建立測試檔案**：
```python
# tests/CBO/ui/test_ui_新功能_cbo.py
from libs.ui_custom_base import CustomBase
from config import TestConfig

class TestUI新功能CBO(CustomBase):
    def test_ui_新功能(self):
        self.specific_window_size()
        login_url = TestConfig.build_ui_url("login", "CBO")
        self.open(login_url)
        self.login("CBO")
        
        # 新功能測試邏輯
        self.click("新功能按鈕選擇器")
        self.assert_element("預期結果選擇器")
        
        self.save_screenshot_with_full_path("新功能測試")
        self.logout("CBO")
```

2. **更新配置檔案**：
在 `test_path_config.yaml` 中新增測試路徑：
```yaml
test_paths:
  cbo_tests:
    - tests/CBO/ui/test_ui_新功能_cbo.py
```

#### 新增 API 測試
1. **建立測試檔案**：
```python
# tests/CBO/api/test_api_新功能_cbo.py
from seleniumbase import BaseCase
import requests
from config import TestConfig

class TestAPI新功能CBO(BaseCase):
    def test_api_新功能(self):
        # API 測試邏輯
        api_url = TestConfig.build_api_url("新路徑", "CBO")
        response = requests.post(api_url, json=payload)
        self.assert_equal(response.status_code, 200)
```

### 2. 新增新平台支援

#### 步驟 1：更新環境變數
在 `.env` 中新增新平台配置：
```env
# 新平台配置
NEW
NEWPLATFORM_LOGIN_URL_UAT=https://new-uat-url.com
NEWPLATFORM_LOGIN_URL_STG=https://new-stg-url.com
NEWPLATFORM_API_URL_UAT=https://new-api-uat-url.com
NEWPLATFORM_API_URL_STG=https://new-api-stg-url.com
NEWPLATFORM_USER_ID=new_user
NEWPLATFORM_PASSWORD=new_password
```

#### 步驟 2：更新 config.py
在 [`TestConfig`](config.py:6) 類別中新增新平台的方法：
```python
@staticmethod
def NEWPLATFORM_LOGIN_URL(): 
    return TestConfig._get_env_specific_value("NEWPLATFORM_LOGIN_URL")

# 在 build_ui_url 方法中新增支援
def build_ui_url(cls, path_key="login", domain_name="KBB"):
    if path_key == "login":
        domain_name_upper = domain_name.upper()
        if domain_name_upper == "NEWPLATFORM":
            return cls.NEWPLATFORM_LOGIN_URL()
        # ... 其他現有平台
```

#### 步驟 3：更新 ui_custom_base.py
在 [`_get_platform_config()`](libs/ui_custom_base.py:107) 方法中新增新平台配置：
```python
platform_configs = {
    "NEWPLATFORM": {
        "user_id": TestConfig.NEWPLATFORM_USER_ID,
        "password": TestConfig.NEWPLATFORM_PASSWORD,
        "user_id_placeholder": "Enter your User ID",
        "password_placeholder": "Enter your Password",
        "logout_selector": "button:contains('Logout')",
    },
    # ... 其他現有平台
}
```

#### 步驟 4：建立測試檔案
建立新平台的測試目錄和檔案：
```bash
mkdir -p tests/NEWPLATFORM/ui
mkdir -p tests/NEWPLATFORM/api
```

#### 步驟 5：更新測試路徑配置
在 [`test_path_config.yaml`](test_path_config.yaml:1) 中新增：
```yaml
test_paths:
  newplatform_tests:
    - tests/NEWPLATFORM/ui/test_ui_登入登出_newplatform.py
    - tests/NEWPLATFORM/api/test_api_登入登出_newplatform.py
```

### 3. 配置修改指南

#### 修改測試環境
1. **切換到 UAT 環境**：
```bash
# 方法 1：修改 .env 檔案
ENVIRONMENT=uat

# 方法 2：執行時指定
ENVIRONMENT=uat python run_test.py
```

2. **切換到 STG 環境**：
```bash
ENVIRONMENT=stg python run_test.py
```

#### 修改瀏覽器設定
```bash
# 使用 Firefox
BROWSER=firefox python run_test.py

# 啟用有頭模式（顯示瀏覽器視窗）
HEADLESS=false python run_test.py
```

#### 修改 Testmo 設定
```env
# 禁用 Testmo 上傳
UPLOAD_TESTMO=false

# 更改 Testmo 專案
TESTMO_PROJECT_ID=新的專案ID
```

### 4. 新增自訂方法

#### 在 CustomBase 中新增通用方法
```python
# libs/ui_custom_base.py
def wait_for_page_load(self, timeout=30):
    """等待頁面完全載入"""
    self.wait_for_ready_state_complete(timeout)

def scroll_to_bottom(self):
    """滾動到頁面底部"""
    self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def clear_browser_cache(self):
    """清除瀏覽器快取"""
    self.execute_script("window.localStorage.clear();")
    self.execute_script("window.sessionStorage.clear();")
```

#### 新增平台特定方法
```python
def click_menu_新功能_cbo(self):
    """點擊 CBO 新功能選單"""
    self.click("span:contains('新功能')")
    self.assert_element("div.新功能容器", timeout=10)
```

### 5. 測試資料管理

#### 建立測試資料檔案
```python
# tests/test_data.py
TEST_USERS = {
    "CBO": {
        "valid_user": {
            "user_id": "test_user_1",
            "password": "test_password_1"
        },
        "invalid_user": {
            "user_id": "invalid_user",
            "password": "invalid_password"
        }
    }
}

TEST_URLS = {
    "CBO": {
        "login_page": "/login",
        "dashboard": "/dashboard",
        "user_management": "/users"
    }
}
```

#### 在測試中使用測試資料
```python
from tests.test_data import TEST_USERS, TEST_URLS

class TestExample(CustomBase):
    def test_with_test_data(self):
        user_data = TEST_USERS["CBO"]["valid_user"]
        self.login("CBO", user_data["user_id"], user_data["password"])
```

---

## 故障排除

### 1. 常見錯誤和解決方案

#### 環境變數相關錯誤

**錯誤訊息**：
```
ValueError: 環境變數 'CBO_LOGIN_URL_STG' 未在 .env 檔案中設定！
```

**解決方案**：
1. 檢查 `.env` 檔案是否存在
2. 確認環境變數名稱拼寫正確
3. 確認 `ENVIRONMENT` 變數設定正確

```bash
# 檢查環境變數
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ENVIRONMENT'))"

# 檢查特定變數
python -c "from config import TestConfig; print(TestConfig.CBO_LOGIN_URL())"
```

#### 瀏覽器驅動問題

**錯誤訊息**：
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**解決方案**：
1. **自動安裝**（推薦）：
```bash
# SeleniumBase 會自動下載驅動
pip install --upgrade seleniumbase
seleniumbase install chromedriver
```

2. **手動安裝**：
```bash
# macOS
brew install chromedriver

# Ubuntu
sudo apt-get install chromium-chromedriver
```

3. **指定驅動路徑**：
```python
# 在測試中指定
self.driver_path = "/path/to/chromedriver"
```

#### 元素定位失敗

**錯誤訊息**：
```
selenium.common.exceptions.NoSuchElementException: Message: no such element
```

**解決方案**：
1. **增加等待時間**：
```python
self.assert_element("選擇器", timeout=30)  # 增加到 30 秒
```

2. **使用更穩定的選擇器**：
```python
# 避免使用
self.click("button")

# 使用更具體的選擇器
self.click("button[data-testid='login-button']")
self.click("button:contains('Login')")
```

3. **新增除錯截圖**：
```python
self.save_screenshot_with_full_path("除錯_元素定位前")
self.click("選擇器")
```

#### 網路連線問題

**錯誤訊息**：
```
requests.exceptions.ConnectionError: Failed to establish a new connection
```

**解決方案**：
1. **檢查網路連線**：
```bash
ping google.com
curl -I https://目標網站.com
```

2. **檢查 VPN 或代理設定**
3. **增加重試機制**：
```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
```

#### Testmo 上傳失敗

**錯誤訊息**：
```
Testmo CLI 未安裝，請執行：sudo npm install -g @testmo/testmo-cli
```

**解決方案**：
1. **安裝 Testmo CLI**：
```bash
sudo npm install -g @testmo/testmo-cli
```

2. **驗證安裝**：
```bash
testmo --version
```

3. **檢查權限**：
```bash
# 確認有寫入權限
ls -la reports/
```

4. **暫時禁用 Testmo**：
```bash
UPLOAD_TESTMO=false python run_test.py
```

### 2. 效能問題

#### 測試執行緩慢

**原因分析**：
- 網路延遲
- 頁面載入時間長
- 等待時間設定過長

**解決方案**：
1. **優化等待時間**：
```python
# 減少不必要的等待
self.assert_element("選擇器", timeout=5)  # 從 10 秒減少到 5 秒

# 使用更精確的等待條件
self.wait_for_element_visible("選擇器", timeout=10)
```

2. **使用無頭模式**：
```bash
HEADLESS=true python run_test.py
```

3. **並行執行**：
```bash
pip install pytest-xdist
pytest -n 4 tests/ -v
```

#### 記憶體使用過高

**解決方案**：
1. **清理瀏覽器資源**：
```python
def tearDown(self):
    self.clear_browser_cache()
    super().tearDown()
```

2. **限制並行數量**：
```bash
pytest -n 2 tests/ -v  # 減少並行數量
```

### 3. 除錯技巧

#### 啟用詳細日誌
```bash
# 啟用 pytest 詳細輸出
pytest -v -s tests/

# 啟用 SeleniumBase 除錯模式
pytest --debug tests/
```

#### 使用互動式除錯
```python
# 在測試中新增斷點
import pdb; pdb.set_trace()

# 或使用 ipdb（需安裝）
import ipdb; ipdb.set_trace()
```

#### 截圖除錯
```python
def test_debug_example(self):
    self.open("https://example.com")
    self.save_screenshot_with_full_path("步驟1_頁面載入")
    
    self.click("button")
    self.save_screenshot_with_full_path("步驟2_點擊按鈕後")
    
    # 檢查元素是否存在
    if self.is_element_present("錯誤訊息選擇器"):
        self.save_screenshot_with_full_path("錯誤_發現錯誤訊息")
```

#### 元素檢查工具
```python
def debug_element_info(self, selector):
    """除錯用：顯示元素資訊"""
    try:
        element = self.find_element(selector)
        print(f"元素找到: {selector}")
        print(f"元素文字: {element.text}")
        print(f"元素屬性: {element.get_attribute('outerHTML')}")
    except Exception as e:
        print(f"元素未找到: {selector}, 錯誤: {e}")
        
        # 列出頁面上所有相似的元素
        similar_elements = self.find_elements("*")
        for elem in similar_elements:
            if selector.lower() in elem.get_attribute('outerHTML').lower():
                print(f"相似元素: {elem.get_attribute('outerHTML')[:100]}...")
```

### 4. 最佳實踐建議

#### 測試穩定性
1. **使用穩定的選擇器**：
   - 優先使用 `data-testid` 屬性
   - 避免使用易變的 CSS 類別名稱
   - 使用文字內容選擇器時要考慮多語言

2. **適當的等待策略**：
   - 使用顯式等待而非固定延遲
   - 根據實際需求調整超時時間
   - 在關鍵操作前後新增檢查點

3. **錯誤處理**：
   - 在關鍵步驟新增 try-catch
   - 提供有意義的錯誤訊息
   - 失敗時自動截圖

#### 程式碼維護
1. **模組化設計**：
   - 將常用操作封裝成方法
   - 使用頁面物件模式（Page Object Pattern）
   - 分離測試資料和測試邏輯

2. **命名規範**：
   - 使用描述性的測試方法名稱
   - 統一的檔案命名格式
   - 清晰的變數和方法命名

3. **文件維護**：
   - 及時更新配置檔案
   - 記錄重要的變更
   - 提供清晰的使用範例

#### 團隊協作
1. **版本控制**：
   - 不要提交 `.env` 檔案
   - 提供 `.env.example` 範本
   - 使用 `.gitignore` 排除敏感檔案

2. **環境一致性**：
   - 使用 `requirements.txt` 鎖定版本
   - 提供環境設置指南
   - 定期更新依賴套件

3. **測試報告**：
   - 定期檢查 Testmo 報告
   - 分析失敗趨勢
   - 及時修復不穩定的測試

---

## 附錄

### A. 環境變數完整清單

#### 必要變數
```env
ENVIRONMENT=stg|uat                          # 執行環境
TEST_MODE=all|ui|api|cbo|kbb|cc             # 測試模式
BROWSER=chrome|firefox|edge                 # 瀏覽器類型
HEADLESS=true|false                         # 無頭模式
```

#### 平台 URL 變數
```env
# CBO 平台
CBO_LOGIN_URL_UAT=https://...
CBO_LOGIN_URL_STG=https://...
CBO_API_URL_UAT=https://...
CBO_API_URL_STG=https://...

# KBB 平台
KBB_LOGIN_URL_UAT=https://...
KBB_LOGIN_URL_STG=https://...
KBB_API_URL_UAT=https://...
KBB_API_URL_STG=https://...

# CC 平台
CCCOMPANY_LOGIN_URL_UAT=https://...
CCCOMPANY_LOGIN_URL_STG=https://...
```

#### 測試帳號變數
```env
# CBO 帳號
CBO_USER_ID=使用者帳號
CBO_PASSWORD=使用者密碼
CBO_ADMIN_USER_ID=管理員帳號
CBO_ADMIN_PASSWORD=管理員密碼
CBO_PLATFORM_CODE=平台代碼

# KBB 帳號
KBB_USER_ID=使用者帳號
KBB_PASSWORD=使用者密碼
KBB_PLATFORM_CODE=平台代碼

# CC 帳號
CCCOMPANY_ADMIN_USER_ID=管理員帳號
CCCOMPANY_ADMIN_PASSWORD=管理員密碼
```

#### Testmo 變數
```env
TESTMO_EMAIL=testmo登入郵箱
TESTMO_EMAIL_PW=gmail應用程式密碼
TESTMO_RECEIVERS=通知接收者郵箱
TESTMO_INSTANCE=testmo實例URL
TESTMO_PROJECT_ID=專案ID
UPLOAD_TESTMO=true|false
```

### B. 常用命令清單

#### 測試執行命令
```bash
# 基本執行
python run_test.py

# 指定環境和模式
ENVIRONMENT=uat TEST_MODE=cbo python run_test.py

# 無頭模式執行
HEADLESS=true python run_test.py

# 禁用 Testmo 上傳
UPLOAD_TESTMO=false python run_test.py

# 使用 pytest 直接執行
pytest tests/CBO/ui/ -v
pytest tests/CBO/api/ -v
pytest -m "smoke" -v
```

#### 環境檢查命令
```bash
# 檢查 Python 版本
python --version

# 檢查套件安裝
pip list | grep selenium
pip list | grep pytest

# 檢查瀏覽器驅動
which chromedriver
chromedriver --version

# 檢查 Testmo CLI
testmo --version
```

#### 除錯命令
```bash
# 詳細輸出
pytest -v -s tests/

# 除錯模式
pytest --debug tests/

# 顯示本地變數
pytest --tb=long tests/

# 停在第一個失敗
pytest -x tests/
```

### C. 選擇器參考

#### 常用 CSS 選擇器
```css
/* 基本選擇器 */
input[placeholder='Enter your User ID']     /* 屬性選擇器 */
button:contains('Login')                    /* 文字內容選擇器 */
.el-button--primary                         /* 類別選擇器 */
#login-form                                 /* ID 選擇器 */

/* 組合選擇器 */
div.user_box > span                         /* 子元素選擇器 */
li.el-dropdown-menu__item:contains('Logout') /* 複合選擇器 */

/* 偽類選擇器 */
button:not(:disabled)                       /* 非禁用按鈕 */
input:focus                                 /* 聚焦的輸入框 */
```

#### XPath 選擇器
```xpath
//button[text()='Login']                    /* 文字內容 */
//input[@placeholder='Enter your User ID'] /* 屬性匹配 */
//div[contains(@class, 'user_box')]         /* 包含類別 */
//tr[.//td[contains(., 'dkyuan_all')]]      /* 複雜條件 */
```

### D. 版本更新記錄

#### v1.0.0 (2024-01-01)
- 初始版本發布
- 支援 CBO、KBB 平台
- 基本 UI 和 API 測試功能

#### v1.1.0 (2024-02-01)
- 新增 CC 平台支援
- 整合 Testmo 報告系統
- 新增郵件通知功能

#### v1.2.0 (2024-03-01)
- 優化截圖功能
- 新增多環境支援
- 改善錯誤處理機制

---

**文件版本**：v1.2.0  
**最後更新**：2024-03-01  
**維護者**：EMB 自動化測試團隊  
**聯絡方式**：derek.yuan@embplc.com