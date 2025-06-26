import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI密碼修改失敗CBO(CustomBase):
    
    def test_ui_changepassword_duplicated(self):

        # =====設定瀏覽器視窗大小 =====
        self.specific_window_size_max()

         # 使用 CBO UI 網域
        login_url = TestConfig.build_ui_url("login", "CBO")
        self.open(login_url)
        
        self.login_page_check_cbo()
        # ===== 第二階段：執行使用者登入流程 =====
        
        self.login_cbo()

        # ===== 第三階段：進入密碼修改功能 =====
        
        # 點擊密碼修改按鈕，開啟密碼修改側邊欄
        # password_draw_btn 是密碼修改按鈕的 CSS 類別
        self.click_resetpassword_cbo()
        
        # ===== 第四階段：輸入重複密碼並提交 =====
        
        self.type_duplicated_password_cbo()
        
        # ===== 第六階段：登出並驗證返回登入頁面 =====
        
        self.logout_cbo()

        print(f"使用的 URL: {login_url}")