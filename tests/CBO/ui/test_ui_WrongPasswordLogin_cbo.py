import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI密碼修改失敗CBO(CustomBase):
    
    def test_ui_wrongid_wrongpassword(self):

        # =====設定瀏覽器視窗大小 =====
        self.specific_window_size_max()

         # 使用 KBB UI 網域
        login_url = TestConfig.build_ui_url("login", "CBO")
        self.open(login_url)
        
        self.login_page_check_cbo()

        # ===== 第二階段：執行使用者登入流程 =====
        
        self.type_wrong_user_id_cbo()

        self.save_screenshot_with_full_path()

        self.type_wrong_password_cbo()

        self.save_screenshot_with_full_path()

        print(f"使用的 URL: {login_url}")