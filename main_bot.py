from requests import session
import urllib3
import urllib.request
from core.constant.base_facebook import Request
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from core.google_api.google_sheet_handler import GoogleSheetHandler

request = session()
gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
post_link = {}
users = []
spreadsheet_name = "new post link"


# def set_comment(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text("Nhập đường dẫn bài viết")
#     if update.callback_query:
#         print(update.callback_query.message)

def get_message_of_id(documents, update):
    chat_id = str(update.message.chat.id)
    for c_id in documents:
        if chat_id == c_id:
            return update.message.text.strip().lower()

def get_ip_public(update: Update, context: CallbackContext) -> None:
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    update.message.reply_text(f"Your ip public {external_ip}")

def other(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global post_link
    global users
    chat_id = str(update.message.chat.id)
    last_name = update.message.chat.last_name
    first_name = update.message.chat.first_name
    name = f"{last_name} {first_name}"
    if name not in users:
        users.append(name)
    try:
        message = update.message.text.strip().lower()
    except AttributeError:
        return
    if "https" in message:
        if "m.facebook" in message:
            message = message.replace("m.", "")
        post_link.update({chat_id: message})
        all_value = GoogleSheetHandler("GROUPS_MANAGER").read_all("post link used")
        all_bot = len(all_value[0])
        post_link_commented_count = len([v for value in all_value[1:] for v in value if message in v])
        update.message.reply_text(f"bài post này bạn còn {all_bot - post_link_commented_count} comments")
    else:
        message = get_message_of_id(post_link, update)
        url = f'http://{Request.API_SERVICE}/comments/add_comment'
        try:
            request.post(url=url, json={
                "post_link": post_link[chat_id],
                "comment": message
            })
        except urllib3.exceptions.MaxRetryError as error:
            print("urllib3: ", error)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5342613247:AAFpznc_Y8pF_0NzZivrBMcjbApZh1yCHjc")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("set_comment", set_comment))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(CommandHandler("ip_public", get_ip_public))
    dispatcher.add_handler(MessageHandler(Filters.all, other))

    # Start the Bot
    updater.start_polling()
    updater.idle()


main()
