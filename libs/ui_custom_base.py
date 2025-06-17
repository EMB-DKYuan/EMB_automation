from seleniumbase import BaseCase
from config import TestConfig

class CustomBase(BaseCase):
    
    def login_page_check_cbo(self):

        # 驗證登入按鈕是否存在，確保頁面已正確載入
        self.assert_element("button:contains('Login')", timeout=10)
        
        # 驗證頁面LOGO元素是否存在
        self.assert_element("img.logo[src='https://mg-web.bhcbo.uat/e3c47/images/login/logo.png']", timeout=10)
    
    def login_cbo(self, user_id=TestConfig.CBO_USER_ID, password=TestConfig.CBO_PASSWORD):

        # 在使用者 ID 輸入框中輸入帳號
        self.type("input[placeholder='Enter your User ID']", user_id)
        
        # 在密碼輸入框中輸入密碼
        self.type("input[placeholder='Enter your Password']", password)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        # 驗證登入成功：檢查登出按鈕是否出現
        self.assert_element("img.icon[src='https://mg-web.bhcbo.uat/e3c47/images/navbar/ic-Exit.svg']", timeout=10)
    
    def login_cbo_admin(self, user_id=TestConfig.CBO_ADMIN_USER_ID, password=TestConfig.CBO_ADMIN_PASSWORD):

        # 在使用者 ID 輸入框中輸入帳號
        self.type("input[placeholder='Enter your User ID']", user_id)
        
        # 在密碼輸入框中輸入密碼
        self.type("input[placeholder='Enter your Password']", password)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        # 驗證登入成功：檢查登出按鈕是否出現
        self.assert_element("img.icon[src='https://mg-web.bhcbo.uat/e3c47/images/navbar/ic-Exit.svg']", timeout=10)

    def logout_cbo(self):

        # 點擊登出按鈕，結束當前會話
        self.click("img.icon[src='https://mg-web.bhcbo.uat/e3c47/images/navbar/ic-Exit.svg']")
        # 驗證已成功登出：檢查登入按鈕是否重新出現
        self.assert_element("button:contains('Login')", timeout=10)
        # 驗證頁面LOGO元素是否存在
        self.assert_element("img.logo[src='https://mg-web.bhcbo.uat/e3c47/images/login/logo.png']", timeout=10)
    
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

    def click_menu_accountmanagement_accountlist_cbo(self):
        # 點擊左側菜單中的 "Account Management" 選項
        self.assert_element("span:contains('Account Management')", timeout=10)
        self.click("span:contains('Account Management')")

        self.assert_element("span:contains('Account List')", timeout=10)
        self.click("span:contains('Account List')")

    def admin_reset_password_dkyuan_all_cbo(self):
        
        target_menu_selector = "//tr[.//td[contains(., 'dkyuan_all')]]//div[contains(@class, 'el-dropdown')]"
        self.click(target_menu_selector)

        self.assert_element("li.el-dropdown-menu__item:contains('Update Password')", timeout=10)
        self.click("li.el-dropdown-menu__item:contains('Update Password')")

        self.assert_element("span.el-drawer__title:contains('Update Password')", timeout=10)

        self.assert_element("input[placeholder='Enter your new password']", timeout=10)
        self.type("input[placeholder='Enter your new password']", TestConfig.CBO_PASSWORD_2)

        self.assert_element("input[placeholder='Enter your new password again']", timeout=10)
        self.type("input[placeholder='Enter your new password again']", TestConfig.CBO_PASSWORD_2)

        self.assert_element_not_present("button.submit:disabled", timeout=10)
        self.assert_element("button.submit", timeout=10)
        self.click("button.submit")

        self.click("div.el-overlay")
        self.assert_element("h2.el-notification__title:contains('Password updated successfully.Password has been reset.')", timeout=10)

################################################################################################################

    def login_page_check_kbb(self):
        
        self.assert_element("button:contains('Login')", timeout=10)
        
        # 驗證頁面副標題元素是否存在
        # 這是頁面身份識別的重要元素，確保載入的是正確的頁面
        self.assert_element("div.subtitle:contains('Centralized Back Office')", timeout=10)
        
        # 驗證副標題的文字內容是否完全正確
        # 這是額外的文字內容驗證，確保頁面內容無誤
        self.assert_text("Centralized Back Office", "div.subtitle")

    def login_kbb(self, user_id=TestConfig.KBB_USER_ID, password=TestConfig.KBB_PASSWORD):
        # 在使用者 ID 輸入框中輸入帳號
        self.type("input[placeholder='Enter your User ID']", user_id)
        
        # 在密碼輸入框中輸入密碼
        self.type("input[placeholder='Enter your Password']", password)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        
        # 驗證登入成功：檢查登出按鈕是否出現
        self.assert_element("button:contains('Logout')", timeout=10)

    def logout_kbb(self):
        # 點擊登出按鈕，結束當前的使用者會話
        self.click("button:contains('Logout')")
        
        # 驗證已成功登出：檢查登入按鈕是否重新出現
        self.assert_element("button:contains('Login')", timeout=10)
        
        # 驗證頁面副標題元素是否重新出現
        self.assert_element("div.subtitle:contains('Centralized Back Office')", timeout=10)
        
        # 最終驗證：確認副標題文字內容正確
        self.assert_text("Centralized Back Office", "div.subtitle")

    def type_wrong_user_id_kbb(self):

        # 在使用者 ID 輸入框中輸入錯誤的帳號
        self.type("input[placeholder='Enter your User ID']", TestConfig.WRONG_USER_ID)
        
        # 在密碼輸入框中輸入正確的密碼
        self.type("input[placeholder='Enter your Password']",  TestConfig.KBB_PASSWORD)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        
        # 驗證錯誤提示訊息是否正確顯示
        self.assert_element("div.error_message:contains('You have entered the wrong user ID or password. Please try again.')", timeout=10)

    def type_wrong_password_kbb(self):

        # 在使用者 ID 輸入框中輸入正確的帳號
        self.type("input[placeholder='Enter your User ID']", TestConfig.KBB_USER_ID)
        
        # 在密碼輸入框中輸入錯誤的密碼
        self.type("input[placeholder='Enter your Password']",  TestConfig.WRONG_PASSWORD)
        
        # 點擊登入按鈕提交登入表單
        self.click("button:contains('Login')")
        
        # 驗證錯誤提示訊息是否正確顯示
        self.assert_element("div.error_message:contains('You have entered the wrong user ID or password. Please try again.')", timeout=10)

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