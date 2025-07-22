# config.py - 移除測試路徑部分
import os
from dotenv import load_dotenv

load_dotenv()
class TestConfig:

    # 讀取環境變數，預設為 'uat'
    ENVIRONMENT = os.getenv("ENVIRONMENT", "uat").upper()

    @classmethod
    def _get_env_specific_value(cls, base_var_name):
        """
        根據當前環境動態獲取配置值。
        例如，若 ENVIRONMENT="STG"，調用 _get_env_specific_value("CBO_LOGIN_URL")
        會嘗試獲取 os.getenv("CBO_LOGIN_URL_STG")。
        """
        var_name = f"{base_var_name}_{cls.ENVIRONMENT}"
        value = os.getenv(var_name)
        print(f"[Config] Reading env var: '{var_name}' -> '{value}'") # 可選：打開此行來輔助除錯
        if value is None:
            raise ValueError(f"環境變數 '{var_name}' 未在 .env 檔案中設定！")
        return value

    # --- 動態屬性：根據環境自動返回對應的值 ---
    @staticmethod
    def CBO_LOGIN_URL(): return TestConfig._get_env_specific_value("CBO_LOGIN_URL")
    @staticmethod
    def KBB_LOGIN_URL(): return TestConfig._get_env_specific_value("KBB_LOGIN_URL")
    @staticmethod
    def CCCOMPANY_LOGIN_URL(): return TestConfig._get_env_specific_value("CCCOMPANY_LOGIN_URL")
    @staticmethod
    def CCAGENT_LOGIN_URL(): return TestConfig._get_env_specific_value("CCAGENT_LOGIN_URL")

    # --- 動態頁面元素 URL ---
    @staticmethod
    def CBO_LOGO_URL(): return TestConfig._get_env_specific_value("CBO_LOGO_URL")
    @staticmethod
    def CBO_LOGOUT_ICON_URL(): return TestConfig._get_env_specific_value("CBO_LOGOUT_ICON_URL")
    @staticmethod
    def CC_LOGO_URL(): return TestConfig._get_env_specific_value("CC_LOGO_URL")
    @staticmethod
    def CC_LOGOUT_ICON_URL(): return TestConfig._get_env_specific_value("CC_LOGOUT_ICON_URL")

    # --- API 路徑配置 (共用) ---
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
    CCCOMPANY_ADMIN_USER_ID = os.getenv("CCCOMPANY_ADMIN_USER_ID", "")
    CCCOMPANY_ADMIN_PASSWORD = os.getenv("CCCOMPANY_ADMIN_PASSWORD", "")
    CCAGENT_ADMIN_USER_ID = os.getenv("CCAGENT_ADMIN_USER_ID", "")
    CCAGENT_ADMIN_PASSWORD = os.getenv("CCAGENT_ADMIN_PASSWORD", "")
    CBO_PLATFORM_CODE = os.getenv("CBO_PLATFORM_CODE", "")
    LOGOUT_UID = os.getenv("LOGOUT_UID", "")
    WRONG_USER_ID = os.getenv("WRONG_USER_ID", "")
    WRONG_PASSWORD = os.getenv("WRONG_PASSWORD", "")

    # --- 額外測試帳號集 (可擴充) ---
    CBO_MULTI_USERS = [
        {"id": os.getenv("CBO_USER_ID"), "pw": os.getenv("CBO_PASSWORD")},
        # 您可以在此處新增更多使用者，或從 .env 讀取
        # {"id": os.getenv("CBO_USER_2_ID"), "pw": os.getenv("CBO_USER_2_PW")},
    ]

################################UI方法##############################
    # URL 生成方法
    @classmethod
    def build_ui_url(cls, path_key="login", domain_name="KBB"):
        """
        根據 domain_name 獲取對應的 UI 登入 URL。
        此方法保持不變是為了向下相容現有的測試案例。
        """
        if path_key == "login":
            domain_name_upper = domain_name.upper()
            if domain_name_upper == "CBO":
                return cls.CBO_LOGIN_URL()
            elif domain_name_upper == "KBB":
                return cls.KBB_LOGIN_URL()
            elif domain_name_upper == "CCCOMPANY":
                return cls.CCCOMPANY_LOGIN_URL()
            elif domain_name_upper == "CCAGENT":
                return cls.CCAGENT_LOGIN_URL()
        raise ValueError(f"未知的 UI URL 組合: path='{path_key}', domain='{domain_name}'")

#################################API方法############################
    @classmethod
    def build_api_url(cls, path_key="login", domain_name="KBB"):
        """動態生成完整的 API URL"""
        base_url = cls._get_env_specific_value(f"{domain_name.upper()}_API_URL")

        path_map = {
            "login": cls.API_LOGIN_PATH,
            "logout": cls.API_LOGOUT_PATH,
            "password": cls.API_PASSWORD_PATH
        }
        path = path_map.get(path_key)

        if path is None:
            raise ValueError(f"未知的 API 路徑類型: '{path_key}'")

        return f"{base_url}{path}"