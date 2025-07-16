import os
from config import TestConfig
from libs.ui_custom_base import CustomBase

class TestUI全頁面點擊CBO(CustomBase):
    
    def test_ui_click(self):

        # =====設定瀏覽器視窗大小 =====
        self.specific_window_size()

         # 使用 CBO UI 網域
        login_url = TestConfig.build_ui_url("login", "CBO")
        self.open(login_url)
        
        self.login_page_check("CBO")

        # ===== 第二階段：執行使用者登入流程 =====
        
        self.login("CBO")

        self.click_menu_accountmanagement_cbo()

        self.click_menu_accountmanagement_accountregistration_cbo()

        self.click_menu_accountmanagement_accountlist_cbo()

        self.click_accountlist_platform_cbo()

        self.click_accountlist_platform_all_cbo()

        self.accountlist_search_button_cbo()

        self.save_screenshot_with_full_path()

        self.click_accountlist_platform_cbo()

        self.click_accountlist_platform_bethub_cbo()

        self.accountlist_search_button_cbo()

        self.save_screenshot_with_full_path()

        self.click_accountlist_platform_cbo()

        self.click_accountlist_platform_bethub2_cbo()

        self.accountlist_search_button_cbo()

        self.save_screenshot_with_full_path()

        self.click_accountlist_platform_cbo()

        self.click_accountlist_platform_playpal_cbo()

        self.accountlist_search_button_cbo()

        self.save_screenshot_with_full_path()

        self.click_accountlist_platform_cbo()

        self.click_accountlist_platform_pin77_cbo()

        self.accountlist_search_button_cbo()

        self.save_screenshot_with_full_path()

        self.click_menu_outletlist_cbo()

        self.click_menu_playerlist_cbo()

        self.click_menu_gamelist_cbo()

        self.click_menu_report_cbo()

        self.logout("CBO")

        print(f"使用的 URL: {login_url}")