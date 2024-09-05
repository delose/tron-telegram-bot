import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

from tronpy import Tron

from tronpy.providers import HTTPProvider

from tronpy.keys import PrivateKey

import json

import os



# Set your TronGrid API key

TRONGRID_API_KEY: Final = os.getenv('TRONGRID_API_KEY')
TELEGRAM_TOKEN: Final = os.getenv('TELEGRAM_TOKEN')

# A simple dictionary to store user wallet data

user_wallets = {}



# Function to generate a Tron wallet

def generate_wallet():

    client = Tron(provider=HTTPProvider(api_key=TRONGRID_API_KEY))

    wallet = client.generate_address()

    address = wallet['base58check_address']

    private_key = wallet['private_key']

    return address, private_key



# Function to get TRX balance of a wallet

def get_trx_balance(address: str) -> float:

    try:

        client = Tron(provider=HTTPProvider(api_key=TRONGRID_API_KEY))

        balance = client.get_account_balance(address)

        return balance

    except Exception as e:

        print(f"Error fetching TRX balance: {e}")

        return 0.0



# Define the /start command handler

async def start(update: Update, context: CallbackContext) -> None:

    user_id = str(update.message.from_user.id)  # Convert user_id to string for consistent dictionary keys



    # Load existing wallet data (if available)

    if os.path.exists('user_wallets.json'):

        with open('user_wallets.json', 'r') as f:

            global user_wallets

            user_wallets = json.load(f)



    if user_id not in user_wallets:

        # Generate a new wallet for the user

        address, private_key = generate_wallet()

        user_wallets[user_id] = {

            'address': address,

            'private_key': private_key

        }

        # Save the user wallet info (for persistence)

        with open('user_wallets.json', 'w') as f:

            json.dump(user_wallets, f)

    else:

        # Use the existing wallet

        address = user_wallets[user_id]['address']

        private_key = user_wallets[user_id]['private_key']



    # Get the current TRX balance

    trx_balance = get_trx_balance(address)



    welcome_message = (

        "Welcome to TronBot\n"

        "Tron's fastest bot to trade any coin!\n\n"

        "Your TronBot wallet address:\n"

        f"{address} (tap to copy)\n\n"

        f"Current TRX Balance: {trx_balance} TRX\n\n"

        "Once done, tap refresh and your balance will appear here.\n\n"

        "To buy a token enter token address, or a URL from sunpump or sun.io\n\n"

        "For more info on your wallet and to retrieve your private key, tap the wallet button below. "

        "User funds are safe on TronBot, but if you expose your private key we can't protect you!"

    )

    

    # Create the inline keyboard buttons

    keyboard = [

        [

            InlineKeyboardButton("Buy", callback_data='buy'),

            InlineKeyboardButton("Sell & Manage", callback_data='sell_manage'),

            InlineKeyboardButton("Community", callback_data='community')

        ],

        [

            InlineKeyboardButton("Refer Friends", callback_data='refer_friends'),

            InlineKeyboardButton("📦 Backup Bots", callback_data='backup_bots')

        ],

        [

            InlineKeyboardButton("Wallet", callback_data='wallet'),

            InlineKeyboardButton("Settings", callback_data='settings')

        ],

        [

            InlineKeyboardButton("Pin", callback_data='pin'),

            InlineKeyboardButton("Refresh", callback_data='refresh')

        ]

    ]

    

    reply_markup = InlineKeyboardMarkup(keyboard)

    

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)



# Function to get token information from SunPump API

async def get_token_info(contract_address_or_url: str):

    api_url = f"https://api-v2.sunpump.meme/pump-api/token/{contract_address_or_url}"

    

    try:

        response = requests.get(api_url)

        if response.status_code == 200:

            data = response.json().get("data", {})

            # Extract the necessary information

            token_name = data.get('name', 'N/A')

            token_symbol = data.get('symbol', 'N/A')

            price_in_trx = data.get('priceInTrx', 'N/A')

            market_cap = data.get('marketCap', 'N/A')

            liquidity = data.get('liquidity', 'N/A')

            listed_on_sunswap = data.get('listedOnSunSwap', False)

            return {

                'name': token_name,

                'symbol': token_symbol,

                'price_in_trx': price_in_trx,

                'market_cap': market_cap,

                'liquidity': liquidity,

                'listed_on_sunswap': listed_on_sunswap,

                'address': contract_address_or_url

            }

        else:

            print(f"Error: Received response code {response.status_code}")

    except Exception as e:

        print(f"Error fetching token info: {e}")

    return None



# Function to display detailed token information

async def display_token_info(update: Update, context: CallbackContext, token_info: dict) -> None:

    status_icon = "✅" if token_info['listed_on_sunswap'] else "❌"

    user_id = str(update.message.from_user.id)

    address = user_wallets[user_id]['address']

    trx_balance = get_trx_balance(address)

    

    token_message = (

        f"{token_info['name']} | {token_info['symbol']} | {token_info['address']}\n"

        f"Listed on SunSwap: {status_icon}\n\n"

        f"Price: {token_info['price_in_trx']}\n"

        f"Market Cap: {token_info['market_cap']}\n"

        f"Liquidity: {token_info['liquidity']}\n"

        f"Wallet Balance: {trx_balance} TRX\n"

        "To buy, press one of the buttons below."

    )



    # Create interactive buttons

    keyboard = [

        [

            InlineKeyboardButton("Explorer", callback_data=f'explorer_{token_info["address"]}'),

            InlineKeyboardButton("Sun.io", callback_data=f'sunio_{token_info["address"]}')

        ],

        [

            InlineKeyboardButton("Buy 5 TRX", callback_data=f'buy_5_{token_info["address"]}'),

            InlineKeyboardButton("Buy 1000 TRX", callback_data=f'buy_1000_{token_info["address"]}')

        ],

        [

            InlineKeyboardButton("Buy 2000 TRX", callback_data=f'buy_2000_{token_info["address"]}'),

            InlineKeyboardButton("Buy 5000 TRX", callback_data=f'buy_5000_{token_info["address"]}')

        ],

        [

            InlineKeyboardButton("Buy X TRX", callback_data=f'buy_x_{token_info["address"]}')

        ],

        [InlineKeyboardButton("Cancel", callback_data='cancel')],

        [InlineKeyboardButton("Refresh", callback_data='refresh')]

    ]



    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(token_message, reply_markup=reply_markup)



# Function to handle messages containing contract addresses or URLs

async def handle_contract_address(update: Update, context: CallbackContext) -> None:

    user_message = update.message.text.strip()



    # Extract the contract address from the URL if necessary

    if "sunpump.meme" in user_message:

        contract_address = user_message.split('/')[-1]

    else:

        contract_address = user_message



    # Fetch token information

    token_info = await get_token_info(contract_address)

    if token_info:

        await display_token_info(update, context, token_info)

    else:

        await update.message.reply_text("Sorry, I couldn't retrieve information for the provided address.")



# Function to handle button clicks (e.g., buying tokens, refreshing info)

# Function to handle button clicks (e.g., buying tokens, refreshing info)

async def button(update: Update, context: CallbackContext) -> None:

    query = update.callback_query

    await query.answer()



    user_id = str(query.from_user.id)



    if user_id not in user_wallets:

        await query.edit_message_text(text="Wallet not found. Please start the bot with /start.")

        return



    user_wallet = user_wallets[user_id]

    private_key = user_wallet['private_key']

    address = user_wallet['address']



    if query.data.startswith('explorer_'):

        # Extract the contract address and generate Tronscan URL

        contract_address = query.data.split('_')[1]

        explorer_url = f"https://tronscan.org/#/contract/{contract_address}"

        await query.edit_message_text(text=f"View this token on Tronscan: {explorer_url}")



    elif query.data.startswith('buy_'):

        _, amount, token_address = query.data.split('_')

        if amount == 'x':

            # Prompt user to input the amount of TRX

            context.user_data['token_address'] = token_address

            await query.edit_message_text(text="Please enter the amount of TRX you want to use for the purchase:")

            return

        else:

            await query.edit_message_text(text=f"Attempting to buy {amount} TRX worth of tokens for {token_address}...")

            contract_address = "TQHj5QZA8PaHBcAGkYdi8QxdtuNabuVx5r"  # The actual contract address for purchases

            success = await purchase_token(contract_address, int(amount), private_key, address)

            if success:

                await query.edit_message_text(text=f"Successfully bought {amount} TRX worth of tokens for {token_address}!")

            else:

                await query.edit_message_text(text=f"Failed to buy {amount} TRX worth of tokens for {token_address}.")

    

    elif query.data == 'cancel':

        await query.edit_message_text(text="Operation canceled.")

    elif query.data == 'refresh':

        trx_balance = get_trx_balance(address)

        await query.edit_message_text(text=f"Refreshed! Current TRX Balance: {trx_balance} TRX")

    elif query.data == 'sunio':

        await query.edit_message_text(text="Opening Sun.io...")

        # Add logic to open Sun.io here



# Function to handle user input for custom TRX amount

async def handle_custom_trx_amount(update: Update, context: CallbackContext) -> None:

    user_id = str(update.message.from_user.id)

    amount_text = update.message.text.strip()



    try:

        amount = int(amount_text)

        if amount <= 0:

            raise ValueError("Amount must be positive.")



        contract_address = context.user_data.get('contract_address')

        if not contract_address:

            await update.message.reply_text("Contract address not found. Please try again.")

            return



        user_wallet = user_wallets[user_id]

        private_key = user_wallet['private_key']

        address = user_wallet['address']



        await update.message.reply_text(f"Attempting to buy {amount} TRX worth of tokens for {contract_address}...")

        success = await purchase_token(contract_address, amount, private_key, address)

        if success:

            await update.message.reply_text(f"Successfully bought {amount} TRX worth of tokens for {contract_address}!")

        else:

            await update.message.reply_text(f"Failed to buy {amount} TRX worth of tokens for {contract_address}.")

    except ValueError:

        await update.message.reply_text("Invalid input. Please enter a valid number for the amount of TRX.")



# Function to buy tokens using TronPy with the user's wallet details

async def purchase_token(contract_address: str, trx_amount: int, private_key: str, my_address: str) -> bool:

    try:

        client = Tron(provider=HTTPProvider(api_key=TRONGRID_API_KEY))



        # Check if the wallet has enough TRX balance

        balance = get_trx_balance(my_address)

        if balance < trx_amount:

            print("Insufficient TRX balance.")

            return False


        # Load the ABI from the JSON file

        with open('abi.json', 'r') as file:
            abi = json.load(file)


        # Load the contract using ABI

        contract = client.get_contract(contract_address, abi=abi)

        

        print(f"Contract loaded: {contract}")

        print(f"Contract functions: {contract.functions}")



        # Build and send the transaction

        txn = (

            contract.functions.purchaseToken(contract_address, trx_amount)

            .with_owner(my_address)

            .fee_limit(100_000_000)

            .call_value(trx_amount * 1_000_000)  # Convert TRX to sun (1 TRX = 1,000,000 sun)

            .build()

            .sign(PrivateKey(bytes.fromhex(private_key)))

            .broadcast()

        )

        

        print(f"Transaction sent: {txn}")



        # Wait for the transaction to be confirmed

        result = txn.wait()

        print(f"Transaction result: {result}")



        return result['receipt']['result']

    except Exception as e:

        print(f"Error purchasing token: {e}")

        import traceback

        traceback.print_exc()

        return False





# Main function to start the bot

def main() -> None:

    application = Application.builder().token(TELEGRAM_TOKEN).build()



    # Register the /start command handler

    application.add_handler(CommandHandler("start", start))



    # Register the message handler for contract addresses or URLs

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contract_address))



    # Register the callback query handler for button clicks

    application.add_handler(CallbackQueryHandler(button))



    # Register the message handler for custom TRX amount input

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_trx_amount))



    # Start the bot

    application.run_polling()



if __name__ == '__main__':

    main()

