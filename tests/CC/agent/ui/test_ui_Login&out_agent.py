import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI登入登出CBO(CustomBase):
    
    def test_ui_login_logout(self):
        
        # =====設定瀏覽器視窗大小 =====
        self.specific_window_size()
        
        # 使用 CCCOMPANY UI 網域
        login_url = TestConfig.build_ui_url("login", "CCAGENT")
        # ===== 第一階段：開啟登入頁面並驗證頁面載入 =====
        self.open(login_url)
        self.login_page_check("CCAGENT")
        self.save_screenshot_with_full_path()

        # ===== 第二階段：輸入使用者憑證並執行登入 =====
        
        self.login("CCAGENT")
        self.save_screenshot_with_full_path()
        
        # ===== 第四階段：執行登出操作 =====
        
        self.logout("CCAGENT")
        self.save_screenshot_with_full_path()
        print(f"使用的 URL: {login_url}")