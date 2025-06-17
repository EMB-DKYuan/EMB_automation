import requests

class APIClient:
    """
    API 客戶端工具類
    
    封裝了 HTTP 請求的常用操作，提供統一的 API 呼叫介面
    支援自動 URL 拼接和靈活的請求參數配置
    """
    
    def __init__(self, base_url):
        """
        初始化 API 客戶端
        
        Args:
            base_url (str): API 的基礎 URL，例如 "https://api.example.com"
                           所有相對路徑的請求都會以此為基礎進行拼接
        
        Example:
            client = APIClient("https://api.example.com")
        """
        # 儲存基礎 URL，用於後續請求的 URL 拼接
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        """
        發送 HTTP 請求
        
        這是一個通用的請求方法，支援所有 HTTP 方法（GET, POST, PUT, DELETE 等）
        會自動處理 URL 拼接邏輯，支援相對路徑和絕對路徑
        
        Args:
            method (str): HTTP 請求方法，例如 "GET", "POST", "PUT", "DELETE"
            url (str): 請求的 URL 路徑
                      - 如果是相對路徑（如 "/users"），會自動與 base_url 拼接
                      - 如果是絕對路徑（如 "https://other-api.com/data"），會直接使用
            **kwargs: 其他請求參數，會直接傳遞給 requests.request() 方法
                     常用參數包括：
                     - headers (dict): 請求標頭
                     - params (dict): URL 查詢參數
                     - json (dict): JSON 請求體
                     - data (dict): 表單數據
                     - timeout (int): 請求超時時間
                     - verify (bool): 是否驗證 SSL 證書
        
        Returns:
            requests.Response: HTTP 響應物件，包含狀態碼、響應內容等資訊
        
        Example:
            # GET 請求
            response = client.request("GET", "/users", params={"page": 1})
            
            # POST 請求
            response = client.request("POST", "/users", 
                                    json={"name": "John", "email": "john@example.com"},
                                    headers={"Authorization": "Bearer token"})
            
            # 使用絕對 URL
            response = client.request("GET", "https://external-api.com/data")
        """
        # 檢查 URL 是否為絕對路徑（以 "http" 開頭）
        if not url.startswith("http"):
            # 如果是相對路徑，則與基礎 URL 進行拼接
            # 例如：base_url="https://api.example.com", url="/users"
            # 結果：url="https://api.example.com/users"
            url = f"{self.base_url}{url}"
        
        # 使用 requests 模組發送 HTTP 請求
        # method: HTTP 方法
        # url: 完整的請求 URL
        # **kwargs: 展開所有額外的關鍵字參數傳遞給 requests.request()
        return requests.request(method, url, **kwargs)


# 使用範例：
"""
# 初始化 API 客戶端
api_client = APIClient("https://jsonplaceholder.typicode.com")

try:
    # GET 請求 - 獲取所有用戶
    response = api_client.request("GET", "/users")
    if response.status_code == 200:
        users = response.json()
        print(f"獲取到 {len(users)} 個用戶")
    
    # POST 請求 - 創建新用戶
    new_user = {
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com"
    }
    response = api_client.request("POST", "/users", 
                                json=new_user,
                                headers={"Content-Type": "application/json"})
    
    if response.status_code == 201:
        created_user = response.json()
        print(f"成功創建用戶，ID: {created_user.get('id')}")
    
    # PUT 請求 - 更新用戶資料
    updated_data = {"name": "John Smith"}
    response = api_client.request("PUT", "/users/1", 
                                json=updated_data,
                                timeout=30)
    
    # DELETE 請求 - 刪除用戶
    response = api_client.request("DELETE", "/users/1")
    
    # 使用絕對 URL 呼叫外部 API
    response = api_client.request("GET", "https://httpbin.org/ip")
    
except requests.exceptions.RequestException as e:
    print(f"請求失敗: {e}")
except requests.exceptions.Timeout:
    print("請求超時")
except requests.exceptions.ConnectionError:
    print("連線錯誤")
"""


# 擴展範例 - 常用的便利方法：
"""
class APIClient:
    # ... 原有代碼 ...
    
    def get(self, url, **kwargs):
        \"\"\"發送 GET 請求的便利方法\"\"\"
        return self.request("GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        \"\"\"發送 POST 請求的便利方法\"\"\"
        return self.request("POST", url, **kwargs)
    
    def put(self, url, **kwargs):
        \"\"\"發送 PUT 請求的便利方法\"\"\"
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url, **kwargs):
        \"\"\"發送 DELETE 請求的便利方法\"\"\"
        return self.request("DELETE", url, **kwargs)
"""
