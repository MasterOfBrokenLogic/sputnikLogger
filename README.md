# Sputnik Key logger v2

![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/<MasterOfBrokenLogic>/<sputnik>)


## Disclaimer

This script is designed to gather browser-related data, including login credentials, cookies, web history, and download information. It also includes functionality to send this data via Telegram for educational and research purposes only. **Unauthorized use of this script may violate privacy laws. Ensure you have appropriate permissions before running this script.**

## Overview

This Python script collects various data from installed browsers on a Windows system and sends it via Telegram. It supports the following browsers:

- Google Chrome
- Microsoft Edge
- Firefox
- Brave
- Opera

## Features

- **Data Collection**: Retrieves login credentials, credit card details, cookies, web history, and download information from supported browsers.
- **Encryption**: Utilizes AES encryption for sensitive data.
- **Telegram Integration**: Sends collected data securely via Telegram bot API.

## Installation

1. **Clone the repository**:
git clone <repository-url>
cd <repository-name>

2. **Install dependencies**:
pip install -r requirements.txt

3. **Configure Telegram bot**:
- Obtain a Telegram Bot token from [BotFather](https://t.me/BotFather).
- Replace `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` in the script with your bot token and chat ID.

## Usage

1. **Run the script**:
sputnikLogger.py

2. **Monitor script output**:
- The script will collect data from installed browsers.
- Data will be sent securely to Telegram if configured.

## Security Considerations

- **Encryption**: Uses AES encryption for secure data handling.
- **Token Security**: Handle Telegram bot tokens securely to prevent unauthorized access.
- **Data Privacy**: Respect user privacy and legal requirements when deploying this script.

## Disclaimer

This script is for educational and research purposes only. Ensure compliance with local laws and obtain proper authorization before using it. The author assumes no liability for unauthorized or illegal use of this script.
