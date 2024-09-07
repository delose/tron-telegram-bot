# TronBot - A Telegram Bot for Trading Tokens on the Tron Network

TronBot is a Python-based Telegram bot designed for trading tokens on the Tron blockchain. It allows users to generate wallets, check balances, and buy tokens using TRX, directly from the Telegram interface.

## Features

- Generate Tron Wallets: Each user gets a unique Tron wallet address upon starting the bot.
- Check TRX Balance: Users can check the balance of their Tron wallet.
- Buy Tokens: The bot allows users to buy tokens by interacting with smart contracts on the Tron blockchain.
- Interactive UI: The bot provides an easy-to-use interface with buttons for various actions like buying, selling, and refreshing balances.

## Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.8 or higher
- pip for managing Python packages
- A Telegram Bot Token (obtained from @BotFather on Telegram)
- A TronGrid API Key

## Installation

1. Set Up a Virtual Environment:

   It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment using the appropriate commands for your operating system.

2. Install Required Dependencies:

   Install the required Python packages by running pip install with the necessary package names. If you have a `requirements.txt` file, you can use it to install all dependencies at once.

3. Set Up Environment Variables:

   Create a `.env` file in the project root directory. This file should include your Telegram bot token and TronGrid API key, formatted as follows:

   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   TRONGRID_API_KEY=your_trongrid_api_key
   ```

   Replace `your_telegram_bot_token` with your actual Telegram bot token and `your_trongrid_api_key` with your TronGrid API key.

## How to Run the Bot

   - Run the Bot:

   Start the bot by running the appropriate command in your terminal or command prompt to execute the main Python script. The bot will begin polling for messages and interactions on Telegram.

## How to Run the Python Script

Follow these steps to run the Python script for the TronBot:

1. **Activate the Virtual Environment:**

   Before running the script, ensure that your virtual environment is activated.

   - On **Windows**:
     ```
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```
     source venv/bin/activate
     ```

2. **Run the Python Script:**

   Once the virtual environment is activated, navigate to the directory where your Python script is located (e.g., `src/bot.py`) and run the script using the following command: 
    ```
    python src/tron_bot.py
    ```
3. **📋 Click the button below to copy the commands:**
   ```
   venv\Scripts\activate (Windows)
   source venv/bin/activate (macOS/Linux)
   python src/tron_bot.py
   ```

## Usage

1. Start the Bot:

   Send the `/start` command to the bot on Telegram. This will generate a Tron wallet for you and display your TRX balance.

2. Buy Tokens:

   Provide a token contract address or a URL from supported platforms (like SunPump or Sun.io), and the bot will retrieve the token information. You can then choose to buy tokens using the provided buttons.

3. Manage Your Wallet:

   Use the provided buttons in the bot's UI to manage your wallet, buy or sell tokens, or refresh your balance.

## Troubleshooting

- Insufficient Balance: Ensure your Tron wallet has enough TRX before attempting to buy tokens.
- API Errors: If the bot cannot fetch token information, verify that the provided contract address or URL is correct and that the TronGrid API is reachable.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

## Diagram of the Bot's Functionality

   ```
   +-------------------------------------+
   | User (Telegram)                     |
   |                                     |
   | Sends Command /start, /buy, etc.    |
   +-------------|-----------------------+
               |
               v
   +-------------------------------------+
   | Telegram Bot (Python Script)        |
   |                                     |
   | 1. Generate Wallet                  |
   | 2. Check Wallet Balance             |
   | 3. Handle Commands                  |
   | 4. Store Wallet Data (JSON)         |
   | 5. Interact with Tron Blockchain    |
   +-------------|-----------------------+
               |
               v
   +-------------------------------------+
   | TronPy Client (Python Library)      |
   |                                     |
   | Interacts with the Tron Blockchain  |
   | using TronGrid API                  |
   +-------------|-----------------------+
               |
               v
   +-------------------------------------+
   | Tron Blockchain                     |
   |                                     |
   | 1. Generate Wallet (Address, PK)    |
   | 2. Check Balance                    |
   | 3. Interact with Smart Contracts    |
   +-------------------------------------+
               |
               v
   +-------------------------------------+
   | User Funds Wallet Manually          |
   | (Using TronLink, etc.)              |
   +-------------------------------------+
   ```

## Directory Structure
   ```
   tron-telegram-bot/
   │
   ├── src/tron_bot.py              # Main script for running the bot
   ├── samples/welcome.py              # Sample script for handling Telegram messages
   ├── .env                # Environment variables
   └── abi.json            # ABI file
   ```
