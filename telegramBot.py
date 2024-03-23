import logging
from telegram.ext import Updater, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from myTokens import * 


# Define a custom formatter to include API name in the log messages
formatter = logging.Formatter('%(asctime)s - a:%(name)s - %(levelname)s - API: %(funcName)s - %(message)s')

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add a stream handler to log to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def start(update, context):
    logger.info('in start')
    update.message.reply_text('Hi! Use /random to get a random TED Talk.')

def random_talk(update, context):
    logger.info('reached random_talk')
    update.message.reply_text('Good work bro, now go to /write ')

# Function to handle the /write command
def write_to_google_sheet(update, context):
    # Authenticate with Google Sheets using the credentials JSON file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_JSON_FILE, scope)
    client = gspread.authorize(creds)

    # Open the specified Google Sheet
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

    # Get the message sent by the user
    message_text = update.message.text

    # Write the message to the Google Sheet
    sheet.append_row([message_text])

    # Send a response to the user

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("random", random_talk))
    dispatcher.add_handler(CommandHandler("write", write_to_google_sheet))

    updater.start_polling()
    logger.info('Bot started')

    updater.idle()

if __name__ == '__main__':
    main()


    update.message.reply_text('Message written to Google Sheet successfully!')