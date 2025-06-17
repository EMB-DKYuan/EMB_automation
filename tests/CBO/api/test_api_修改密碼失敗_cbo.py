# 導入 SeleniumBase 的 BaseCase 基礎測試類別
from seleniumbase import BaseCase
import requests
from config import TestConfig

class TestAPI_修改密碼失敗_KBB(BaseCase):

    def test_api_login(self):
        # 使用 KBB 網域
        login_url = TestConfig.build_api_url("login", "CBO")
        
        # 登入請求資料
        payload = {
            "userId": TestConfig.CBO_USER_ID,
            "password": TestConfig.CBO_PASSWORD,
            "platformCode": TestConfig.CBO_PLATFORM_CODE
        }
        
        # 請求標頭
        headers = {"Content-Type": "application/json"}
        
        try:
            # 發送登入請求
            response = requests.post(login_url, headers=headers, json=payload, verify=False)
            
            # 驗證狀態碼
            self.assert_equal(response.status_code, 200)
            
            # 儲存回應和請求資料
            self.login_response = response
            self.login_payload = payload
            
            # 提取回傳資料
            response_data = response.json()
            data = response_data.get("data", {})
            
            self.user_id = data.get("userId")
            self.token = data.get("token")
            self.role = data.get("role")
            self.platform = data.get("platform")
            self.message = response_data.get("message")
            self.code = response_data.get("code")
            
            # 驗證提取的資料
            self.assert_true(self.user_id is not None, "userId 提取失敗")
            self.assert_true(self.token is not None, "token 提取失敗")
            self.assert_equal(self.code, 200, "業務狀態碼不正確")
            self.assert_equal(self.message, "SUCCESS", "回應訊息不正確")
            
            print(f"登入成功 - userId: {self.user_id}, role: {self.role}")
            print(f"使用的 URL: {login_url}")

        except Exception as e:
            print(f"登入失敗: {e}")
            self.user_id = None
            self.token = None

    def test_api_duplicated(self):

        # 確保已有登入資料
        if not hasattr(self, 'token') or not self.token:
            self.test_api_login()
        
        # 使用 KBB 網域
        password_url = TestConfig.build_api_url("password", "KBB")

        # 包含授權令牌的請求標頭
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Uid": TestConfig.CBO_USER_ID
        }
        # 準備登入請求的 payload（請求體數據）
        payload = {
            "oldPassword": TestConfig.CBO_PASSWORD,
            "newPassword":TestConfig.CBO_PASSWORD,
            "confirmNewPassword": TestConfig.CBO_PASSWORD,
            "platformCode": TestConfig.CBO_PLATFORM_CODE
        }
        
        response = requests.post(
            password_url,           # API 端點 URL
            headers=headers,   # HTTP 請求標頭
            json=payload,      # JSON 格式的請求體
            verify=False       # 不驗證 SSL 證書（測試環境常用設定）
        )
        
        # 驗證預期失敗
        self.assert_true(response.status_code in [200], "預期修改密碼失敗")
        self.assert_equal(response.json().get("message"), "New password must be different from your original password.")  # 驗證訊息
        
        print(f"使用的 user_id: {self.user_id}")
        print(f"使用的 token: {self.token}")
        
        # 驗證響應 JSON 中的業務狀態碼
        # self.assert_true(response.json().get("code") == 0)
        
        # 其他可能的驗證項目：
        # self.assert_true("accessToken" in response.json())  # 驗證是否返回存取令牌
        # self.assert_true("refreshToken" in response.json()) # 驗證是否返回刷新令牌
        # self.assert_equal(response.json().get("message"), "登入成功")  # 驗證成功訊息
        
        # 可以印出響應內容以便調試（在開發階段使用）
        # print(f"響應狀態碼: {response.status_code}")
        # print(f"響應內容: {response.json()}")

    def test_api_logout(self):
        
        # 確保已有登入資料
        if not hasattr(self, 'token') or not self.token:
            self.test_api_login()
        
        # 使用 KBB 網域
        logout_url = TestConfig.build_api_url("logout", "KBB")
        
        # 包含授權令牌的請求標頭
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Uid": TestConfig.LOGOUT_UID
        }
        
        # 發送登出請求
        logout_response = requests.post(logout_url, headers=headers, verify=False)
        
        # 驗證登出成功
        self.assert_equal(logout_response.status_code, 200)
        print("登出成功")
        print(f"使用的 URL: {logout_url}")