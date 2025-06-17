import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI登入登出KBB(CustomBase):
    
    def test_ui_login_logout(self):
        

        # 使用 KBB UI 網域
        login_url = TestConfig.build_ui_url("login", "KBB")
        # ===== 第一階段：開啟登入頁面並驗證頁面載入 =====
        self.open(login_url)
        
        # 驗證登入按鈕是否存在，確保頁面已正確載入
        self.login_page_check_kbb()
        
        # ===== 第二階段：輸入使用者憑證並執行登入 =====
        
        self.login_kbb()
        
        # ===== 第四階段：執行登出操作 =====
        
        self.logout_kbb()
        # 驗證已成功登出：檢查登入按鈕是否重新出現

        print(f"使用的 URL: {login_url}")