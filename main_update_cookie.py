from json import dumps
import sys
import time
from json import dumps as json_dumps, loads
import logging
from telegram import Bot
from telegram.error import TelegramError
from sn.facebook.functions.update_fb_cookie.update_cookie import UpdateCookie
from sn.facebook.functions.update_fb_cookie.get_token import GetToken
from core.google_api.google_sheet_handler import GoogleSheetHandler

gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
cookie_spreadsheet_name = "FB Cookies"
token_spreadsheet_name = "FB Token"
sms_spreadsheet_name = "FB SMS"
phone_spreadsheet_name = "FB Phone"
"""telegram"""
TOKEN = "5675446466:AAEBBUGxuUunLuyy4sI6Y6sv62obNJeaIdE"
GROUP_CHAT_ID = "-861616656"
def send_message(chat_id, text):
    bot = Bot(TOKEN)
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        logging.error(e)
phone_number = gg_sheet_handler.read(phone_spreadsheet_name, sys.argv[1].strip())
if not phone_number:
    exit(0)
else:
    phone_number = phone_number[0].strip()

""" Get cookie """
raw_cookie = gg_sheet_handler.read(cookie_spreadsheet_name, sys.argv[1].strip())
raw_cookie = raw_cookie[0].strip() if raw_cookie else None
cookies = json_dumps(UpdateCookie(raw_cookie).update_new_cookie())
gg_sheet_handler.over_write(cookie_spreadsheet_name, sys.argv[1].strip(), cookies)
""" Get token """
token = gg_sheet_handler.read(token_spreadsheet_name, sys.argv[1].strip())
print("token before: ", token)
if not token:
    raw_cookie = gg_sheet_handler.read(cookie_spreadsheet_name, sys.argv[1].strip())
    raw_cookie = raw_cookie[0].strip() if raw_cookie else None
    if raw_cookie:
        gtk = GetToken(loads(raw_cookie))
        token = gtk.get_token()
        if not token:
            uck = UpdateCookie(raw_cookie)
            while True:
                sms = gg_sheet_handler.read(sms_spreadsheet_name, sys.argv[1].strip())
                sms = sms[0].strip() if sms else None
                verify_status = uck.fill_verify_sms(sms)
                print("verify_status: ",  verify_status)
                if not verify_status:
                    send_message(GROUP_CHAT_ID, f"tài khoản {sys.argv[1].strip()} cần xác thực\n"
                                                f"số điện thoai: {phone_number}")
                    time.sleep(30)

                else:
                    uck.browser_handler.save_cookie()
                    cookie = uck.browser_handler.get_cookie()
                    gg_sheet_handler.over_write(cookie_spreadsheet_name,
                                                sys.argv[1].strip(),
                                                dumps(cookie))
                    gtk = GetToken(cookie)
                    token = gtk.get_token()
                    gg_sheet_handler.over_write(token_spreadsheet_name,
                                                sys.argv[1].strip(), token)
                    break
                time.sleep(60)
            uck.browser_handler.close_driver()
        gg_sheet_handler.over_write(token_spreadsheet_name, sys.argv[1].strip(), token)
