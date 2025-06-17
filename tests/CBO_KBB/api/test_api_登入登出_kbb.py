from seleniumbase import BaseCase
import requests
from config import TestConfig

class TestAPI_登入登出_KBB(BaseCase):
    """API 登入登出測試類別"""
    
    def test_api_login(self):
        # 使用 KBB 網域
        login_url = TestConfig.build_api_url("login", "KBB")
        
        # 登入請求資料
        payload = {
            "userId": TestConfig.KBB_USER_ID,
            "password": TestConfig.KBB_PASSWORD,
            "platformCode": TestConfig.KBB_PLATFORM_CODE
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