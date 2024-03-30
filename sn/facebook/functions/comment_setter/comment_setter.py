import time
from re import sub as re_sub
from requests import HTTPError
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import FacebookUrl, FacebookXPath


class comment_setter_w_selenium(object):
    def __init__(self):
        self.cookies_file_name = "cookies_selenium.txt"
        self.group_link_file_name = "group_post_link.txt"
        self.post_link_file = "post_link.txt"
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler()
        self.browser_handler.set_driver_option()

    def comment(self, text_box, name, all_level, skip_level=None, list_comment=[]):
        for idx, _ in enumerate(range(all_level)):
            if skip_level and skip_level == idx + 1:
                continue
            comment = list_comment.pop()
            text_box.send_keys(self.browser_handler.keys.TAB, "@")
            [text_box.send_keys(self.browser_handler.keys.TAB, name_char) for name_char in name]
            time.sleep(2)
            [text_box.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.ARROW_DOWN) for _ in
             range(idx)]
            time.sleep(1)
            text_box.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.ENTER)
            time.sleep(1)
            text_box.send_keys(self.browser_handler.keys.TAB, " ")
            [text_box.send_keys(self.browser_handler.keys.TAB, char) for char in comment]
            time.sleep(2)
            text_box.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.ENTER)
            # text_box.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.CONTROL, "a")
            # time.sleep(1)
            # text_box.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.BACK_SPACE)

    def send_post_link_to_chat_room(self, post_link, chat_room_id):
        self.login()
        if not self.join_chat_room:
            self.browser_handler.open_url("https://www.facebook.com/messages/t/{}".format(chat_room_id))
            self.join_chat_room = True
        self.browser_handler.web_drive_wait_until(FacebookXPath.CHOOSE_A_GIF_LABEL, 60)
        time.sleep(10)
        choose_a_gif_label = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.CHOOSE_A_GIF_LABEL)
        [choose_a_gif_label.send_keys(self.browser_handler.keys.TAB, char) for char in post_link]
        choose_a_gif_label.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.ENTER)
        # choose_a_gif_label.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.CONTROL, "a")
        # time.sleep(1)
        # choose_a_gif_label.send_keys(self.browser_handler.keys.TAB, self.browser_handler.keys.BACK_SPACE)

    def tag_comment(self, chat_room_id, name, all_level, skip_level=None, list_comment=[]):
        if not list_comment:
            return
        self.login()
        if not self.join_chat_room:
            self.browser_handler.open_url("https://www.facebook.com/messages/t/{}".format(chat_room_id))
            self.join_chat_room = True
        time.sleep(1)
        self.browser_handler.web_drive_wait_until(FacebookXPath.CHOOSE_A_GIF_LABEL, 60)
        choose_a_gif_label = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.CHOOSE_A_GIF_LABEL)
        self.comment(choose_a_gif_label, name, all_level, skip_level, list_comment)

    def add_link(self, link):
        is_exist = False
        try:
            with open(self.group_link_file_name, "r") as f:
                data = f.read().strip()
                link_list = data.split()
                if link in link_list:
                    is_exist = True
                    return is_exist
                with open(self.group_link_file_name, "a") as f:
                    f.write(f"{link}\n")
                    return is_exist
        except FileNotFoundError:
            with open(self.group_link_file_name, "a") as f:
                f.write(f"{link}\n")
                return is_exist

    @staticmethod
    def convert_message(message_body):
        message_body = re_sub(r"([_*\[\]()~`>\#\+\-=|\.!{}])", r"\\\1", message_body)
        message_body = message_body.replace('%', '\\%25')
        message_body = message_body.replace('#', '\\%23')
        message_body = message_body.replace('+', '\\%2B')
        message_body = message_body.replace('*', '\\%2A')
        message_body = message_body.replace('&', '\\%26')
        return message_body[:150]

    def login(self):
        if self.logged_in_status:
            print(f"Logged in")
            return
        if not self.logged_in_status:
            print(f"Start login")
            login_with_cookies_status = True
            for _ in range(3):
                self.browser_handler.open_url(FacebookUrl.FACEBOOK_URL.format(""))
                time.sleep(15)
                login_with_cookies_status = self.login_with_cookies()
                if login_with_cookies_status:
                    break
            if not login_with_cookies_status:
                self.browser_handler.close_driver()
                raise ValueError("No alive cookies found")
            self.logged_in_status = True

    def login_with_cookies(self):
        print("login with cookies")
        if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.USERNAME_FORM, wait_time=30):
            raise HTTPError(f"{FacebookXPath.USERNAME_FORM} could not found before load cookie")
        load_cookie_status = self.browser_handler.load_cookie(xpath=FacebookXPath.SEARCH_FORM)
        return load_cookie_status
