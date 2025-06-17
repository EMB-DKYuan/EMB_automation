# config.py - 移除測試路徑部分
import os
from dotenv import load_dotenv

load_dotenv()
class TestConfig:

    # 環境設定
    ENVIRONMENT = os.getenv("ENVIRONMENT", "")
    
    # UI 網域配置（使用業務名稱）
    UI_DOMAINS = {
        "CBO": os.getenv("UI_DOMAIN_CBO", ""),
        "KBB": os.getenv("UI_DOMAIN_KBB", "")
    }
    
    # API 網域配置（使用業務名稱）
    API_DOMAINS = {
        "CBO": os.getenv("API_DOMAIN_CBO", ""),
        "KBB": os.getenv("API_DOMAIN_KBB", "")
    }

    # UI 路徑配置
    UI_LOGIN_PATH = os.getenv("UI_LOGIN_PATH", "")
    
    # API 路徑配置
    API_LOGIN_PATH = os.getenv("API_LOGIN_PATH", "")
    API_LOGOUT_PATH = os.getenv("API_LOGOUT_PATH", "")
    API_PASSWORD_PATH = os.getenv("API_PASSWORD_PATH", "")

    # 系統配置
    KBB_USER_ID = os.getenv("KBB_USER_ID", "")
    KBB_PASSWORD = os.getenv("KBB_PASSWORD", "")
    KBB_PLATFORM_CODE = os.getenv("KBB_PLATFORM_CODE", "")
    CBO_USER_ID = os.getenv("CBO_USER_ID", "")
    CBO_PASSWORD = os.getenv("CBO_PASSWORD", "")
    CBO_PASSWORD_2 = os.getenv("CBO_PASSWORD_2", "")
    CBO_ADMIN_USER_ID = os.getenv("CBO_ADMIN_USER_ID", "")
    CBO_ADMIN_PASSWORD = os.getenv("CBO_ADMIN_PASSWORD", "")
    CBO_PLATFORM_CODE = os.getenv("CBO_PLATFORM_CODE", "")
    LOGOUT_UID = os.getenv("LOGOUT_UID", "")
    WRONG_USER_ID = os.getenv("WRONG_USER_ID", "")
    WRONG_PASSWORD = os.getenv("WRONG_PASSWORD", "")
    
    # UI 測試配置
    KBB_LOGIN_URL = os.getenv("KBB_LOGIN_URL", "")
    CBO_LOGIN_URL = os.getenv("CBO_LOGIN_URL", "")
    
    # API 測試配置
    KBB_LOGIN_API_URL = os.getenv("KBB_LOGIN_API_URL", "")
    KBB_LOGOUT_API_URL = os.getenv("KBB_LOGOUT_API_URL", "")
    KBB_PASSWORD_API_URL = os.getenv("KBB_PASSWORD_API_URL", "")
    CBO_LOGIN_API_URL = os.getenv("CBO_LOGIN_API_URL", "")
    CBO_LOGOUT_API_URL = os.getenv("CBO_LOGOUT_API_URL", "")
    CBO_PASSWORD_API_URL = os.getenv("CBO_PASSWORD_API_URL", "")

################################UI方法##############################
    # URL 生成方法
    @classmethod
    def build_ui_url(cls, path_key="login", domain_name="KBB"):
        """生成 UI URL
        
        Args:
            path_key (str): 路徑類型 ("login" 等)
            domain_name (str): 網域名稱 ("CBO", "KBB", "ADMIN")
        """
        path_map = {
            "login": cls.UI_LOGIN_PATH
        }
        path = path_map.get(path_key, path_key)
        
        domain = cls.UI_DOMAINS.get(domain_name.upper(), cls.UI_DOMAINS["KBB"])
        return f"{domain}.{cls.ENVIRONMENT}{path}"
    
    # 便利方法：取得所有網域的 URL
    @classmethod
    def get_all_ui_urls(cls, path_key="login"):
        """取得所有 UI 網域的 URL"""
        return {name: cls.build_ui_url(path_key, name) for name in cls.UI_DOMAINS.keys()}
    

#################################API方法############################
    @classmethod
    def build_api_url(cls, path_key="login", domain_name="KBB"):
        """生成 API URL
        
        Args:
            path_key (str): API 類型 ("login", "logout", "password")
            domain_name (str): 網域名稱 ("CBO", "KBB", "ADMIN")
        """
        path_map = {
            "login": cls.API_LOGIN_PATH,
            "logout": cls.API_LOGOUT_PATH,
            "password": cls.API_PASSWORD_PATH
        }
        path = path_map.get(path_key, path_key)
        
        domain = cls.API_DOMAINS.get(domain_name.upper(), cls.API_DOMAINS["KBB"])
        return f"{domain}.{cls.ENVIRONMENT}{path}"
    
    @classmethod
    def get_all_api_urls(cls, path_key="login"):
        """取得所有 API 網域的 URL"""
        return {name: cls.build_api_url(path_key, name) for name in cls.API_DOMAINS.keys()}