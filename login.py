import base64
import logging

import requests
from colorama import Fore, Style
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def rsa_encrypt_pkcs1v15(data: str, public_key: str) -> str:
    """RSA 加密（PKCS#1 v1.5），公钥支持 PEM 或纯 Base64 格式。"""
    if not public_key.strip().startswith("-----BEGIN"):
        public_key = f"""-----BEGIN PUBLIC KEY-----
{public_key.strip()}
-----END PUBLIC KEY-----"""

    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_bytes = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()
    except (ValueError, IndexError, TypeError) as e:
        raise ValueError("无效的公钥格式") from e


def encrypt(data):
    try:
        key_url = "https://www.baomi.org.cn/portal/main-api/getPublishKey.do"
        response = requests.get(key_url)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}获取公钥失败，状态码: {response.status_code}{Style.RESET_ALL}")
            return None

        public_key = response.json()["data"]
        return rsa_encrypt_pkcs1v15(data, public_key)
    except Exception as e:
        logging.error(f"{Fore.RED}加密过程出错: {e}{Style.RESET_ALL}")
        raise Exception(f"加密数据失败: {e}") from e


def login(loginName, passWord):
    try:
        login_url = "https://www.baomi.org.cn/portal/main-api/loginInNew.do"
        payload = {
            "loginName": encrypt(loginName),
            "passWord": encrypt(passWord),
            "deviceId": 1711,
            "deviceOs": "pc",
            "lon": 40,
            "lat": 30,
            "siteId": "95",
            "sinopec": "false",
        }

        headers = {
            "Content-Type": "application/json",
            "siteId": "95",
        }
        response = requests.post(login_url, json=payload, headers=headers)
        if response.status_code != 200:
            logging.error(f"{Fore.RED}登录请求失败，状态码：{response.status_code}{Style.RESET_ALL}")
            logging.error(f"{Fore.RED}响应内容：{response.text[:500]}{Style.RESET_ALL}")
            raise Exception(f"登录请求失败，状态码：{response.status_code}")

        try:
            response_data = response.json()
        except Exception as je:
            logging.error(f"{Fore.RED}JSON 解析失败：{je}{Style.RESET_ALL}")
            logging.error(f"{Fore.RED}响应内容：{response.text[:500]}{Style.RESET_ALL}")
            raise Exception(f"服务器返回了无效的数据格式")
        
        logging.info(f"{Fore.GREEN}登录响应：{response_data}{Style.RESET_ALL}")
        
        # 检查是否有错误信息
        if response_data is None:
            raise Exception("服务器返回了空响应")
            
        error = response_data.get("error", {}) if isinstance(response_data.get("error"), dict) else {}
        error_msg = error.get("errorMsg", "") if error else ""
        
        if "token" not in response_data or not response_data["token"]:
            if error_msg:
                # 检查是否包含密码错误次数
                if "输错" in error_msg:
                    raise Exception(f"密码错误：{error_msg}")
                else:
                    raise Exception(f"登录失败：{error_msg}")
            else:
                raise Exception("登录失败：未返回 token")

        return response_data["token"]
    except Exception as e:
        logging.error(f"{Fore.RED}登录过程出错：{e}{Style.RESET_ALL}")
        raise
