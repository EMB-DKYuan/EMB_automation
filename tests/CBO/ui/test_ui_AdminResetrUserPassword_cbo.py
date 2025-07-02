import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUIadmin改密碼後user重置密碼CBO(CustomBase):
    
    def test_ui_admin_changepassword_user_resetpassword(self):
        
        # =====設定瀏覽器視窗大小 =====
        self.specific_window_size_max()
        
        # =====使用 KBB UI 網域 =====
        login_url = TestConfig.build_ui_url("login", "CBO")
       
        # =====開啟登入頁面並驗證頁面載入 =====
        self.open(login_url)
        
        self.login_page_check_cbo()

        # =====輸入使用者憑證並執行登入 =====
        
        self.login_cbo_admin()

        # =====admine改密碼 =====

        self.click_menu_accountmanagement_cbo()

        self.click_menu_accountmanagement_accountlist_cbo()

        self.admin_reset_password_dkyuan_all_cbo()

        self.save_screenshot_with_full_path()

        self.admin_recovery_password_dkyuan_all_cbo()
        
        # =====執行登出操作 =====
        
        self.logout_cbo()

        print(f"使用的 URL: {login_url}")