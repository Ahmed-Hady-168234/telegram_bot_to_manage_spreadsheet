import logging
from telegram.ext import Updater, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from myTokens import TELEGRAM_BOT_TOKEN, GOOGLE_SHEETS_JSON_FILE, SPREADSHEET_ID, WORKSHEET_NAME
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegramBot_types import Columns

# Define a custom formatter to include API name in the log messages
formatter = logging.Formatter('%(asctime)s - a:%(name)s - %(levelname)s - API: %(funcName)s - %(message)s')

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add a stream handler to log to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Function to handle the /write command
def write_to_google_sheet(update, context, row, col, text):
    # Authenticate with Google Sheets using the credentials JSON file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_JSON_FILE, scope)
    client = gspread.authorize(creds)

    # Open the specified Google Sheet
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

    # Convert 1-based row and column indices to 0-based indices
    row_index = row - 1
    col_index = col - 1

    # Ensure the row index is within the bounds of the sheet
    if row_index < 0 or row_index >= sheet.row_count:
        logger.info('Invalid row index')
        print("Invalid row index")
        return
    # Ensure the column index is within the bounds of the sheet
    if col_index < 0 or col_index >= sheet.col_count:
        logger.info('Invalid column index')
        print("Invalid column index")
        return

    # Update the specified cell with the provided text
    sheet.update_cell(row_index + 1, col_index + 1, text)  # Adjust indices to 1-based
    logger.info('successfully wrote', text,' at (row,col):(',row,',',col,')')

    # Send a response to the user

def write_command(update, context):
    # Extract command arguments
    try:
        args = context.args
        row = int(args[0])
        col = int(args[1])
        text = ' '.join(args[2:])
    except (ValueError, IndexError):
        update.message.reply_text('Invalid command format. Usage: /write <row> <col> <text>')
        return

    # Pass the arguments to the write_to_google_sheet function
    write_to_google_sheet(update, context, row, col, text)

# Define command handlers
def start(update, context):
    update.message.reply_text('Hello! I am your Google Sheets Bot.')
    # Define the keyboard layout
    keyboard = [
        ['Option 1', 'Option 2'],
        ['Option 3', 'Option 4']
    ]
    # Create the ReplyKeyboardMarkup object
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    # Send the message with the menu
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    # Print a message to the user
    # dispatcher.bot.send_message(chat_id=TELEGRAM_BOT_TOKEN, text="السلام عليكم, ممكن تعمل /ادخال /write .")
    
    dispatcher.add_handler(CommandHandler("a", start))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("write", write_command))
    # dispatcher.add_handler(CommandHandler("ادخال", write_command))

    updater.start_polling()
    logger.info('Bot started')

    updater.idle()

if __name__ == '__main__':
    main()
    update.message.reply_text('Message written to Google Sheet successfully!')