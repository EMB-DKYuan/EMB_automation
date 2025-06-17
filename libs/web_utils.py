# 導入 Selenium WebDriver 相關模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebUtils:
    """
    Web 自動化測試工具類
    
    封裝了 Selenium WebDriver 的常用操作，提供簡化的 API 介面
    支援 Chrome 和 Firefox 瀏覽器，並提供統一的元素定位方式
    """
    
    def __init__(self, browser="chrome", width=1920, height=1080):
        
        # 根據指定的瀏覽器類型初始化對應的 WebDriver
        if browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            # 拋出異常，提示不支援的瀏覽器類型
            raise Exception("Unsupported browser")
        
        # 設定隱式等待時間為 10 秒
        # 當元素未立即找到時，WebDriver 會等待最多 10 秒
        self.driver.implicitly_wait(10)
        
        # 設定瀏覽器視窗大小
        self.driver.set_window_size(width, height)

    def open(self, url):
        """
        開啟指定的網頁 URL
        
        Args:
            url (str): 要開啟的網頁地址
        """
        self.driver.get(url)

    def send_keys(self, locator, text):
        """
        在指定元素中輸入文字
        
        Args:
            locator (str): 元素定位器，格式為 "定位方式=定位值"
                          例如: "xpath=//input[@id='username']" 或 "id=username"
            text (str): 要輸入的文字內容
        
        Note:
            此方法會先清空元素中的現有內容，再輸入新的文字
        """
        # 解析定位器字串，分離定位方式和定位值
        by, value = locator.split("=", 1)
        
        # 根據定位方式找到對應的元素
        # getattr(By, by.upper()) 動態獲取 By 類別中的定位方法
        elem = self.driver.find_element(getattr(By, by.upper()), value)
        
        # 清空元素中的現有內容
        elem.clear()
        
        # 輸入新的文字
        elem.send_keys(text)

    def click(self, locator):
        """
        點擊指定的元素
        
        Args:
            locator (str): 元素定位器，格式為 "定位方式=定位值"
                          例如: "xpath=//button[@id='submit']" 或 "id=submit"
        """
        # 解析定位器字串，分離定位方式和定位值
        by, value = locator.split("=", 1)
        
        # 根據定位方式找到對應的元素並點擊
        elem = self.driver.find_element(getattr(By, by.upper()), value)
        elem.click()

    def verify_element(self, locator, timeout=10):
        """
        驗證指定元素是否存在於頁面中
        
        Args:
            locator (str): 元素定位器，格式為 "定位方式=定位值"
            timeout (int): 等待超時時間（秒），預設為 10 秒
            
        Returns:
            bool: 如果元素在指定時間內出現則返回 True，否則返回 False
        """
        # 解析定位器字串
        by, value = locator.split("=", 1)
        
        try:
            # 使用顯式等待，等待元素出現在 DOM 中
            # WebDriverWait 提供比隱式等待更精確的控制
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((getattr(By, by.upper()), value))
            )
            return True
        except Exception:
            # 如果在指定時間內元素未出現，則返回 False
            return False
    
    def get_element_text(self, locator):
        """
        獲取指定元素的文字內容
        
        Args:
            locator (str): 元素定位器，格式為 "定位方式=定位值"
            
        Returns:
            str: 元素的文字內容
        """
        # 解析定位器字串
        by, value = locator.split("=", 1)
        
        # 找到元素並返回其文字內容
        elem = self.driver.find_element(getattr(By, by.upper()), value)
        return elem.text

    def quit(self):
        """
        關閉瀏覽器並結束 WebDriver 會話
        
        Note:
            此方法會關閉所有瀏覽器視窗並釋放相關資源
            建議在測試結束後總是調用此方法以避免資源洩漏
        """
        self.driver.quit()


# 使用範例：
"""
# 初始化 WebUtils 實例
utils = WebUtils("chrome", 1920, 1080)

try:
    # 開啟網頁
    utils.open("https://example.com")
    
    # 驗證頁面元素是否存在
    if utils.verify_element("id=username"):
        # 輸入使用者名稱
        utils.send_keys("id=username", "testuser")
        
        # 輸入密碼
        utils.send_keys("id=password", "testpass")
        
        # 點擊登入按鈕
        utils.click("xpath=//button[@type='submit']")
        
        # 獲取歡迎訊息文字
        welcome_text = utils.get_element_text("class=welcome-message")
        print(f"歡迎訊息: {welcome_text}")
        
finally:
    # 確保瀏覽器被正確關閉
    utils.quit()
"""
