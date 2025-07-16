from seleniumbase import BaseCase
from config import TestConfig
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dotenv import load_dotenv
import os
import sys
import re
import inspect

class CustomBase(BaseCase):

    def specific_window_size_max(self):
        self.maximize_window()
    
    def specific_window_size(self, width=1920, height=1080):
        """
        設定瀏覽器視窗大小為指定的寬度和高度。
        預設值為 1920x1080。
        """
        self.set_window_size(width, height)
    
    def set_page_zoom(self, level=100):
        """
        設定瀏覽器頁面的縮放層級。
        :param level: 縮放百分比 (例如: 75 就是 75%)
        """
        zoom_level = level / 100.0
        self.execute_script(f"document.body.style.zoom = '{zoom_level}'")
        print(f"頁面縮放已設定為: {level}%")

    def reset_page_zoom(self):
        """ 將頁面縮放恢復為 100% """
        self.set_page_zoom(100)
    
    def set_browser_zoom(self, level=100):
        """
        透過模擬鍵盤操作來設定瀏覽器本身的縮放層級。
        這比修改 CSS 的 'zoom' 屬性更可靠。
        :param level: 目標縮放百分比 (例如: 75, 90, 110)
        """
        # 判斷作業系統，選擇對應的控制鍵 (Ctrl 或 Command)
        control_key = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

        # 2. 先重設縮放為 100%，以建立一個基準點
        self.driver.find_element("tag name", "html").send_keys(control_key, "0")

        # 3. 根據目標層級，決定是放大還是縮小
        if level < 100:
            # 假設每次縮小 10%，計算需要按幾次
            steps = int((100 - level) / 10)
            for _ in range(steps):
                self.driver.find_element("tag name", "html").send_keys(control_key, Keys.SUBTRACT) # Keys.SUBTRACT 是小鍵盤的 '-'
        elif level > 100:
            # 假設每次放大 10%，計算需要按幾次
            steps = int((level - 100) / 10)
            for _ in range(steps):
                self.driver.find_element("tag name", "html").send_keys(control_key, Keys.ADD) # Keys.ADD 是小鍵盤的 '+'
        
        print(f"瀏覽器縮放已嘗試設定至約: {level}%")

    def __init__(self, *args, **kwargs):
        # 這是關鍵第一步：在測試物件初始化時，就建立一個代表本次執行的時間戳
        super().__init__(*args, **kwargs)
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_screenshot_with_full_path(self, task_name=None):
         
        # 取得專案根目錄
        project_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

        # 取得測試模式
        env_path = os.path.join(project_root, '.env')
        load_dotenv(dotenv_path=env_path)
        test_mode = os.getenv("TEST_MODE", "default")

        # 取得呼叫此函式的腳本名稱
        caller_frame = inspect.stack()[1]
        script_path = caller_frame.filename
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        script_name = re.sub(r'[^A-Za-z0-9_\-]', '_', script_name)

        # 這是關鍵第二步：使用 self.run_timestamp 來建立唯一的執行資料夾
        # 路徑結構變為： reports / 執行時間戳 / 測試模式 / 腳本名稱
        full_folder_path = os.path.join(
            project_root, "reports", self.run_timestamp, test_mode, script_name
        )
        os.makedirs(full_folder_path, exist_ok=True)

        # 這是關鍵第三步：為每張圖片建立一個包含毫秒的唯一檔名，防止覆蓋
        file_time_str = datetime.now().strftime("%H%M%S_%f")[:-3]  # 精確到毫秒
        if task_name:
            task_name = re.sub(r'[^A-Za-z0-9_\-]', '_', task_name)
            screenshot_name = f"{file_time_str}_{task_name}.png"
        else:
            screenshot_name = f"{file_time_str}_screenshot.png"

        self.sleep(0.5)

        # 組合完整路徑並存檔
        full_path = os.path.join(full_folder_path, screenshot_name)
        self.save_screenshot(full_path)
        print(f"截圖已儲存至: {full_path}")

################################################################################################################

    def _get_platform_config(self, platform):
        """獲取指定平台的 UI 元素和預設帳密配置"""
        platform = platform.upper()
        # 定義所有平台的配置信息
        platform_configs = {
            "CBO": {
                "user_id": TestConfig.CBO_USER_ID,
                "password": TestConfig.CBO_PASSWORD,
                "admin_user_id": TestConfig.CBO_ADMIN_USER_ID,
                "admin_password": TestConfig.CBO_ADMIN_PASSWORD,
                "user_id_placeholder": "Enter your User ID",
                "password_placeholder": "Enter your Password",
                "logo_selector": f"img.logo[src='{TestConfig.CBO_LOGO_URL()}']",
                "logout_selector": f"img.icon[src='{TestConfig.CBO_LOGOUT_ICON_URL()}']",
            },
            "KBB": {
                "user_id": TestConfig.KBB_USER_ID,
                "password": TestConfig.KBB_PASSWORD,
                "user_id_placeholder": "Enter your User ID",
                "password_placeholder": "Enter your Password",
                "logo_selector": "div.subtitle:contains('Centralized Back Office')",
                "logout_selector": "button:contains('Logout')",
            },
            "CCCOMPANY": {
                "user_id": TestConfig.CCCOMPANY_ADMIN_USER_ID, # 只有 admin
                "password": TestConfig.CCCOMPANY_ADMIN_PASSWORD,
                "user_id_placeholder": "Input your account",
                "password_placeholder": "Enter your password",
                "logo_selector": f"img.logo[src='{TestConfig.CC_LOGO_URL()}']",
                "logout_selector": f"img.icon[src='{TestConfig.CC_LOGOUT_ICON_URL()}']",
            },
            "CCAGENT": {
                "user_id": TestConfig.CCAGENT_ADMIN_USER_ID, # 只有 admin
                "password": TestConfig.CCAGENT_ADMIN_PASSWORD,
                "user_id_placeholder": "Input your account",
                "password_placeholder": "Enter your password",
                "logo_selector": f"img.logo[src='{TestConfig.CC_LOGO_URL()}']", # 假設與 CCCOMPANY 共用
                "logout_selector": f"img.icon[src='{TestConfig.CC_LOGOUT_ICON_URL()}']", # 假設與 CCCOMPANY 共用
            }
        }
        config = platform_configs.get(platform)
        if not config:
            raise ValueError(f"未知的平台配置: '{platform}'")
        return config
    
    def login(self, platform, user_id=None, password=None, is_admin=False):
        """通用的登入方法"""
        config = self._get_platform_config(platform)

        # 根據是否為 admin 決定預設帳密
        if is_admin and "admin_user_id" in config:
            default_user = config["admin_user_id"]
            default_password = config["admin_password"]
        else:
            default_user = config["user_id"]
            default_password = config["password"]
            
        final_user_id = user_id or default_user
        final_password = password or default_password

        self.type(f"input[placeholder='{config['user_id_placeholder']}']", final_user_id)
        self.type(f"input[placeholder='{config['password_placeholder']}']", final_password)
        self.click("button:contains('Login')")
        self.assert_element(config["logout_selector"], timeout=10)

    def logout(self, platform):
        """通用的登出方法"""
        config = self._get_platform_config(platform)
        self.click(config["logout_selector"])
        self.login_page_check(platform)

    def login_page_check(self, platform):
        """通用的登入頁面檢查方法"""
        config = self._get_platform_config(platform)
        self.assert_element("button:contains('Login')", timeout=10)
        self.assert_element(config["logo_selector"], timeout=10)

    def type_wrong_user_id_cbo(self):

        # 在使用者 ID 輸入框中輸入帳號
        self.type("input[placeholder='Enter your User ID']", TestConfig.WRONG_USER_ID)
        
        # 在密碼輸入框中輸入密碼
        self.type("input[placeholder='Enter your Password']",  TestConfig.CBO_PASSWORD)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        self.assert_element("h2.el-notification__title:contains('You have entered the wrong user ID or password. Please try again.')", timeout=10)

    def type_wrong_password_cbo(self):

        # 在使用者 ID 輸入框中輸入帳號
        self.type("input[placeholder='Enter your User ID']", TestConfig.CBO_USER_ID)
        
        # 在密碼輸入框中輸入密碼
        self.type("input[placeholder='Enter your Password']",  TestConfig.WRONG_PASSWORD)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        self.assert_element("h2.el-notification__title:contains('You have entered the wrong user ID or password. Please try again.')", timeout=10)

    def click_resetpassword_cbo(self):

        self.assert_element("div.user_box", timeout=10)
        self.click("div.user_box")

        self.assert_element("li.el-dropdown-menu__item:contains('Reset Password')", timeout=10)
        self.click("li.el-dropdown-menu__item:contains('Reset Password')")
        
        # 驗證密碼修改側邊欄是否正確開啟，檢查側邊欄標題是否顯示 "Change Password"
        self.assert_element("span.el-drawer__title:contains('Reset Password')", timeout=10)

    def type_duplicated_password_cbo(self):
        # 在舊密碼輸入框中輸入當前密碼
        self.type("input[placeholder='Enter your old password']", TestConfig.CBO_PASSWORD)
        
        # 在新密碼輸入框中輸入與舊密碼相同的密碼（故意製造重複）
        self.type("input[placeholder='Enter your new password']", TestConfig.CBO_PASSWORD)
        
        # 在確認新密碼輸入框中再次輸入相同的密碼
        self.type("input[placeholder='Enter your new password again']", TestConfig.CBO_PASSWORD)
        
        # 點擊提交按鈕，嘗試修改密碼
        self.click("button.submit")
        self.assert_element("h2.el-notification__title:contains('New password is duplicated.')", timeout=10)

        # 點擊遮罩層關閉錯誤提示通知
        # el-overlay 是 Element UI 的遮罩層元素
        self.click("div.el-overlay")

    def click_menu_accountmanagement_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Account Management')")
    
    def click_menu_accountmanagement_accountregistration_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Account Registration')")

    def click_menu_accountmanagement_accountlist_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Account List')")

    def accountlist_search_button_cbo(self):

        self.click("span:contains('Search')")

    def click_accountlist_platform_cbo(self):

        self.click("div.el-select__selected-item.el-select__placeholder")
    
    def click_accountlist_platform_all_cbo(self):

        self.click("li.el-select-dropdown__item:contains('All')")
        
    def click_accountlist_platform_bethub_cbo(self):

        self.click("li.el-select-dropdown__item:contains('BETHUB')")

    def click_accountlist_platform_bethub2_cbo(self):

        self.click("li.el-select-dropdown__item:contains('BETHUB2')")

    def click_accountlist_platform_playpal_cbo(self):

        self.click("li.el-select-dropdown__item:contains('PLAYPAL')")

    def click_accountlist_platform_pin77_cbo(self):

        self.click("li.el-select-dropdown__item:contains('Pin77')")

################################################################################################################

    def click_menu_outletlist_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Outlet List')")

    def click_menu_playerlist_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Player List')")

    def click_menu_gamelist_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Game List')")
    
    def click_menu_report_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.click("span:contains('Report')")

    def admin_reset_password_dkyuan_all_cbo(self):
        
        target_menu_selector = "//tr[.//td[contains(., 'dkyuan_all')]]//div[contains(@class, 'el-dropdown')]"
        self.click(target_menu_selector)

        self.click("li.el-dropdown-menu__item:contains('Update Password')")

        self.assert_element("span.el-drawer__title:contains('Update Password')", timeout=10)

        self.type("input[placeholder='Enter your password again']", TestConfig.CBO_PASSWORD_2)

        self.type("input[placeholder='Enter your new password']", TestConfig.CBO_PASSWORD_2)

        self.assert_element_not_present("button.submit:disabled", timeout=10)
        self.assert_element("button.submit", timeout=10)
        self.click("button.submit")

        self.assert_element("h2.el-notification__title:contains('Password changed Successfully.')", timeout=10)
        self.assert_element("div.el-notification__content:contains('Password has been changed.')", timeout=10)

    def admin_recovery_password_dkyuan_all_cbo(self):
     
        target_menu_selector = "//tr[.//td[contains(., 'dkyuan_all')]]//div[contains(@class, 'el-dropdown')]"
        self.click(target_menu_selector)

        self.click("li.el-dropdown-menu__item:contains('Update Password')")

        self.assert_element("span.el-drawer__title:contains('Update Password')", timeout=10)

        self.type("input[placeholder='Enter your password again']", TestConfig.CBO_PASSWORD)

        self.type("input[placeholder='Enter your new password']", TestConfig.CBO_PASSWORD)

        self.assert_element_not_present("button.submit:disabled", timeout=10)
        self.assert_element("button.submit", timeout=10)
        self.click("button.submit")

        self.assert_element("h2.el-notification__title:contains('Password changed Successfully.')", timeout=10)
        self.assert_element("div.el-notification__content:contains('Password has been changed.')", timeout=10)
################################################################################################################

    def click_resetpassword_kbb(self):

        # 點擊密碼修改按鈕，開啟密碼修改側邊欄
        self.click("button.password_draw_btn")
        
        # 驗證密碼修改側邊欄是否正確開啟
        # 檢查側邊欄標題是否顯示 "Change Password"
        self.assert_element("span.el-drawer__title:contains('Change Password')", timeout=10)

    def type_duplicated_password_kbb(self):

        # 在舊密碼輸入框中輸入當前密碼
        self.type("input[placeholder='Enter your old password']", TestConfig.KBB_PASSWORD)
        
        # 在新密碼輸入框中輸入與舊密碼相同的密碼（故意製造重複）
        self.type("input[placeholder='Enter your new password']", TestConfig.KBB_PASSWORD)
        
        # 在確認新密碼輸入框中再次輸入相同的密碼
        self.type("input[placeholder='Enter your new password again']", TestConfig.KBB_PASSWORD)
        
        # 點擊提交按鈕，嘗試修改密碼
        self.click("button.submit")
        
        # 驗證系統是否正確顯示密碼重複的錯誤提示
        self.assert_element("h2.el-notification__title:contains('New password is duplicated.')", timeout=10)
        
        # 點擊遮罩層關閉錯誤提示通知
        self.click("div.el-overlay")

    def cancel_mask(self):

        self.execute_script("""document.querySelectorAll('.el-popper.is-custom_tooltip.el-tooltip, .el-overlay, .el-drawer__mask, .v-modal').forEach(e => e.style.display='none');""")