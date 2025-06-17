import datetime
import os
import smtplib
import subprocess
import re
from email.mime.text import MIMEText
from getpass import getpass
from dotenv import load_dotenv
import yaml

load_dotenv()

TEST_PATHS = os.getenv("TEST_PATHS", "").split(",")
TEST_MARKS = os.getenv("TEST_MARKS", "").strip() or None

SENDER_EMAIL = os.getenv("TESTMO_EMAIL")
EMAIL_PASSWORD = os.getenv("TESTMO_EMAIL_PW")
RECEIVERS = os.getenv("TESTMO_RECEIVERS", "").split(",")
TESTMO_INSTANCE = os.getenv("TESTMO_INSTANCE")
TESTMO_PROJECT_ID = os.getenv("TESTMO_PROJECT_ID")
UPLOAD_TESTMO = os.getenv("UPLOAD_TESTMO", "true").lower() == "true"

def build_pytest_cmd(html_report, xml_report):
    """純粹的 pytest 命令，不包含 SeleniumBase 的 Testmo 參數"""
    cmd = [
        "python3", "-m", "pytest",
        "-v", "--capture=no", "-rP"
    ]
    cmd.extend(TEST_PATHS)
    cmd.extend([
        f"--html={html_report}",
        "--self-contained-html",
        f"--junitxml={xml_report}"
    ])
    if TEST_MARKS:
        cmd.extend(["-m", ",".join(TEST_MARKS)])
    return cmd

def upload_to_testmo(xml_report, timestamp):
    """獨立的 Testmo 上傳函數"""
    if not UPLOAD_TESTMO or not TESTMO_PROJECT_ID:
        return "（Testmo 上傳已禁用）"
    
    if not os.path.exists(xml_report):
        return "（XML 報告不存在，無法上傳）"
    
    try:
        testmo_cmd = [
            "testmo", "automation:run:submit",
            "--instance", TESTMO_INSTANCE,
            "--project-id", str(TESTMO_PROJECT_ID),
            "--name", f"自動化測試_{timestamp}",
            "--source", "pytest",
            "--results", xml_report
        ]
        
        print(f"上傳 Testmo 命令: {' '.join(testmo_cmd)}")
        result = subprocess.run(testmo_cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # 從 Testmo CLI 輸出中提取報告網址
            output = result.stdout + result.stderr
            url_match = re.search(r'(https://\S+/automation/runs/view/\d+)', output)
            if url_match:
                return url_match.group(1)
            else:
                return f"{TESTMO_INSTANCE}/projects/{TESTMO_PROJECT_ID}/automation/runs"
        else:
            return f"Testmo 上傳失敗：{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Testmo 上傳超時"
    except FileNotFoundError:
        return "Testmo CLI 未安裝，請執行：sudo npm install -g @testmo/testmo-cli"
    except Exception as e:
        return f"Testmo 上傳異常：{str(e)}"

def get_test_paths():
    """從 YAML 配置檔案獲取測試路徑"""
    try:
        with open('test_path_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        mode = os.getenv("TEST_MODE", config.get("mode", "all"))
        test_paths = config.get("test_paths", {})
        
        if mode == "all":
            all_tests = []
            for test_list in test_paths.values():
                all_tests.extend(test_list)
            return all_tests
        else:
            return test_paths.get(f"{mode}_tests", [])
    except FileNotFoundError:
        print("test_path_config.yaml 不存在，使用環境變數")
        return os.getenv("TEST_PATHS", "").split(",")

TEST_PATHS = [path.strip() for path in get_test_paths() if path.strip()]

def main():
    os.makedirs('reports', exist_ok=True)
    print(f"報告目錄權限：{oct(os.stat('reports').st_mode)[-3:]}")
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    html_report = f'reports/report_{timestamp}.html'
    xml_report = f'reports/results_{timestamp}.xml'

    # 第一階段：執行 SeleniumBase 測試
    pytest_cmd = build_pytest_cmd(html_report, xml_report)
    print("執行測試命令:", " ".join(pytest_cmd))
    
    pytest_result = 0
    pytest_output = ""
    
    try:
        result = subprocess.run(
            pytest_cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
        pytest_output = result.stdout + "\n" + result.stderr
        pytest_result = result.returncode
        print("[調試] pytest 輸出:\n", pytest_output)
    except subprocess.TimeoutExpired as e:
        pytest_result = 1
        pytest_output = f"測試執行超時！{str(e)}"
    except Exception as e:
        pytest_result = 1
        pytest_output = f"主程序異常：{str(e)}"

    # 檢查報告是否生成
    if not os.path.exists(html_report):
        print(f"[錯誤] HTML 報告未生成：{html_report}")
        with open(html_report, "w") as f:
            f.write(f"<h1>報告生成失敗</h1><pre>{pytest_output}</pre>")

    # 第二階段：獨立上傳到 Testmo
    print("\n開始上傳到 Testmo...")
    testmo_url = upload_to_testmo(xml_report, timestamp)
    print(f"Testmo 上傳結果：{testmo_url}")

    # 第三階段：郵件通知
    if pytest_result != 0:
        sender = SENDER_EMAIL
        password = EMAIL_PASSWORD or getpass("請輸入 Gmail 應用程式密碼: ")
        receivers = [r.strip() for r in RECEIVERS if r.strip()]
        subject = "🚨 SeleniumBase 自動化測試失敗通知"
        body = f"""測試失敗！錯誤摘要：
{pytest_output[:500]}...

Testmo 報告：{testmo_url}
本地 HTML 報告：{os.path.abspath(html_report)}
本地 XML 報告：{os.path.abspath(xml_report)}
"""
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(receivers)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receivers, msg.as_string())
                print("已發送失敗通知 Email")
        except Exception as e:
            print("Email 發送失敗：", e)
    else:
        print("✅ 測試全部通過！")
        print(f"📊 Testmo 報告：{testmo_url}")
        print(f"📄 本地 HTML 報告：{os.path.abspath(html_report)}")
        print(f"📋 本地 XML 報告：{os.path.abspath(xml_report)}")

if __name__ == "__main__":
    main()
