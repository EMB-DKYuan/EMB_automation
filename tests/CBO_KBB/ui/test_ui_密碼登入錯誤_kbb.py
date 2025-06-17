# 導入 SeleniumBase 的 BaseCase 基礎測試類別
from seleniumbase import BaseCase
import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI密碼修改失敗KBB(CustomBase):
    
    def test_ui_wrongid_wrongpassword(self):

         # 使用 KBB UI 網域
        login_url = TestConfig.build_ui_url("login", "KBB")
        self.open(login_url)
        
        self.login_page_check_kbb()

        # ===== 第二階段：執行使用者登入流程 =====
        
        self.type_wrong_user_id_kbb()
        
        self.type_wrong_password_kbb()

        print(f"使用的 URL: {login_url}")