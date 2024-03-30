import random
from requests import session
import urllib3
import time
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from core.constant.base_facebook import Request
from core.util.file_handler import FileHandler
from sn.facebook.functions.comment_setter.comment_setter import comment_setter_w_selenium
from core.request_handler.base_request_handler import BaseRequestHandler

request = session()
cmt_setter = comment_setter_w_selenium()
post_link_global = None
post_link_process_list = []


# request_handler = BaseRequestHandler()


class Main(object):
    def __init__(self):
        self.time_interval_between_sessions = 1 * 60
        self.time_interval_between_groups = 30

    def get_comment(self, restaurant_name):
        url = Request.GOOGLE_API_URL
        payload = {
            "sheet_name": "GROUPS_MANAGER",
            "spread_sheet_name": "comment",
            "field_name": restaurant_name
        }
        response_data = BaseRequestHandler.make_post_request(url=url, payload=payload)
        comment_list = response_data.json()["data"]["field_value"]
        return comment_list

    def comment_list_single(self, comment_list):
        bt_comments = [x.split("-")[-1].strip() for x in comment_list if x.startswith("bt")]
        rv_comments = [x.split("-")[-1].strip() for x in comment_list if x.startswith("rv")]
        random.shuffle(bt_comments)
        random.shuffle(rv_comments)
        return rv_comments[:3] + bt_comments

    # def set_comment_for_nvbc(self, post_link, comment_list):
    #     ### nv ben cang
    #     cmt_setter.send_post_link_to_chat_room(post_link, 6872804676094100)
    #     time.sleep(1)
    #     cmt_setter.tag_comment(6872804676094100, "nguy", all_level=4, skip_level=1, list_comment=comment_list)
    #     time.sleep(1)
    #     cmt_setter.tag_comment(6872804676094100, "huyn", all_level=2, list_comment=comment_list)
    #     time.sleep(1)
    #     cmt_setter.tag_comment(6872804676094100, "linh", all_level=1, list_comment=comment_list)
    #     time.sleep(1)
    #     cmt_setter.tag_comment(6872804676094100, "tu", all_level=1, list_comment=comment_list)
    #     time.sleep(1)
    #     cmt_setter.tag_comment(6872804676094100, "c", all_level=2, list_comment=comment_list)
    #     cmt_setter.join_chat_room = False

    def set_comment_for_nvsg(self, post_link, comment_list):
        ### nv sg
        cmt_setter.send_post_link_to_chat_room(post_link, 3536952666318936)
        time.sleep(1)
        cmt_setter.tag_comment(3536952666318936, "yen", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3536952666318936, "ly", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3536952666318936, "bang", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.join_chat_room = False

    def set_comment_for_nvsg2(self, post_link, comment_list):
        ### nv sg2
        cmt_setter.send_post_link_to_chat_room(post_link, 3359664597391406)
        time.sleep(1)
        cmt_setter.tag_comment(3359664597391406, "vy", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3359664597391406, "quang", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3359664597391406, "lan", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3359664597391406, "quyen", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.join_chat_room = False

    def set_comment_for_nvvhs(self, post_link, comment_list):
        cmt_setter.send_post_link_to_chat_room(post_link, 3358621740849179)
        time.sleep(1)
        ### nv vy hs
        cmt_setter.tag_comment(3358621740849179, "quach", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3358621740849179, "luong", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.tag_comment(3358621740849179, "chi", all_level=1, list_comment=comment_list)
        time.sleep(1)
        cmt_setter.join_chat_room = False

    def set_comment(self, post_link, set_mode):
        vx_comments = self.get_comment("VONGXOAY")
        bc_comments = self.get_comment("BENCANG")
        mix_comments = self.get_comment("MIX")
        if set_mode == "bc":
            print(post_link)
            comment_list = self.comment_list_single(bc_comments)
            self.set_comment_for_nvvhs(post_link, comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg(post_link, comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg2(post_link, comment_list)
            time.sleep(2)
        elif set_mode == "vx":
            print(post_link)
            comment_list = self.comment_list_single(vx_comments)
            self.set_comment_for_nvvhs(post_link, comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg(post_link, comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg2(post_link, comment_list)
            # cmt_setter.tag_comment(5282135838504843, "nguy", all_level=2, list_comment=comment_list)
        elif set_mode == "mix":
            mix_comment_list = self.comment_list_single(mix_comments)
            vx_comment_list = self.comment_list_single(vx_comments)
            bc_comment_list = self.comment_list_single(bc_comments)
            temp = vx_comment_list + bc_comment_list
            random.shuffle(temp)
            mix_comment_list.extend(temp)
            mix_comment_list = mix_comment_list[::-1]
            self.set_comment_for_nvvhs(post_link, mix_comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg(post_link, mix_comment_list)
            time.sleep(2)
            self.set_comment_for_nvsg2(post_link, mix_comment_list)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    message = u"""
        Menu:
        /set_comment - set comment cho các nhóm seeding
    """
    update.message.reply_text(message)
    # print(update.message.text)
    # user = update.effective_user
    # update.message.reply_markdown_v2(
    #     fr'Hi {user.mention_markdown_v2()}\!',
    #     reply_markup=ForceReply(selective=True),
    # )


def set_comment(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Nhập đường dẫn bài viết")
    if update.callback_query:
        print(update.callback_query.message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def other(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global post_link_global
    global post_link_process_list
    main = Main()
    message = update.message.text.strip().lower()
    if "https" in message:
        # post_link_process_list.append(message)
        link_list = FileHandler.read_file(cmt_setter.post_link_file).split("\n")
        if message in link_list:
            update.message.reply_text("bài viết này đã set comment, hãy kiểm tra lại !")
            return
        post_link_global = message
        update.message.reply_text("""
        - Muốn set cho Bến Cảng thì điền: bc
        - Muốn set cho Vòng Xoay thì điền: vx
        - Muốn set cho cả BC và VX thì điền: mix
        - Muốn cmt thì gõ cmt như bt""")
    elif message in ["bc", "vx", "mix"]:
        update.message.reply_text("Đang set comment xin vui lòng đợi ...")
        # FileHandler.write_file(cmt_setter.post_link_file, post_link_global)
        main.set_comment(post_link_global, message)
        cmt_setter.browser_handler.save_cookie()
        update.message.reply_text("Đã hoàn thành tác vụ")
    else:
        url = f'http://{Request.API_SERVICE}/comments/add_comment'
        try:
            request.post(url=url, json={
                "post_link": post_link_global,
                "comment": message
            })
        except urllib3.exceptions.MaxRetryError:
            pass


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5342613247:AAFpznc_Y8pF_0NzZivrBMcjbApZh1yCHjc")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("set_comment", set_comment))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, other))

    # Start the Bot
    updater.start_polling()
    updater.idle()


main()
