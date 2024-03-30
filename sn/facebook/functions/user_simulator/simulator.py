import time
from requests import HTTPError
import random
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import FacebookUrl, FacebookXPath


class simulator(object):
    def __init__(self, cookies=None):
        self.cookies_file_name = "cookies_selenium.txt"
        self.cookies = cookies
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option()

    def comment_action(self, text_box, text):
        [text_box.send_keys(char) for char in text]

    def is_group_ban(self, post_link):
        is_ban = False
        link_ele = post_link.split("/")
        group_link = "/".join([x for x in link_ele[:link_ele.index("groups") + 2]])
        print("check_group_ban: ", group_link)
        self.browser_handler.open_url(group_link)
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.WRITE_SOMETHING], wait_time=30):
            is_ban = True
        return is_ban

    def is_join_group(self):
        return self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.JOINED_GROUP_PATTERN], wait_time=10)


    def comment_on_post(self, link, comment):
        is_post_deleted = False
        if not self.logged_in_status:
            self.login()
        link = link.strip()
        self.browser_handler.open_url(link)
        if not self.is_join_group():
            print("group nay chua tham gia")
            return
        if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.MORE_GROUP_PATTERN], wait_time=10):
            more_group_button = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.MORE_GROUP_PATTERN)
            more_group_button.send_keys(self.browser_handler.keys.SHIFT,
                                        self.browser_handler.keys.TAB, self.browser_handler.keys.ENTER)
            time.sleep(5)
        pattern_write_comment = None
        if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.WRITE_COMMENT_PATTERN], wait_time=30):
            pattern_write_comment = FacebookXPath.WRITE_COMMENT_PATTERN
        elif self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.WRITE_ANSWER_PATTERN], wait_time=30):
            pattern_write_comment = FacebookXPath.WRITE_ANSWER_PATTERN
        if not pattern_write_comment:
            is_group_ban = self.is_group_ban(link)
            if not is_group_ban:
                print("post bi xoa")
                return "deleted"
            else:
                print("bi ban roi")
                return "banned"
        try:
            comment_box = self.browser_handler.driver.find_element_by_xpath(pattern_write_comment)
        except self.browser_handler.exceptions.NoSuchElementException:
            if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.WRITE_PUBLIC_COMMENT_PATTERN], wait_time=10):
                comment_box = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.WRITE_PUBLIC_COMMENT_PATTERN)
        tag_name = None
        comment_sequence = []
        if "bencang" in comment:
            comment_sequence = comment.split("bencang")
            tag_name = "@haisanben"
        if "vongxoay" in comment:
            comment_sequence = comment.split("vongxoay")
            tag_name = "@vongxoayseafood"
        if tag_name:
            self.comment_action(comment_box, "".join(comment_sequence[0]))
            time.sleep(2)
            self.comment_action(comment_box, tag_name)
            time.sleep(5)
            if tag_name == "@haisanben":
                comment_box.send_keys(self.browser_handler.keys.ARROW_DOWN)
                time.sleep(1)
            comment_box.send_keys(self.browser_handler.keys.ENTER)
            time.sleep(2)
            self.comment_action(comment_box, "".join(comment_sequence[-1]))
            time.sleep(2)
            comment_box.send_keys(self.browser_handler.keys.ENTER)
            time.sleep(2)
        else:
            self.comment_action(comment_box, comment)
            time.sleep(2)
            comment_box.send_keys(self.browser_handler.keys.ENTER)
            time.sleep(2)
        return is_post_deleted

    def random_action(self):
        true = [True] * 60
        false = [False] * 40
        temp = true + false
        random.shuffle(temp)
        return random.choice(temp)

    def like_action(self):
        try:
            like_buttons = self.browser_handler.driver.find_elements_by_xpath(FacebookXPath.LIKE_BUTTON)
        except self.browser_handler.exceptions.NoSuchElementException:
            like_buttons = None
        except self.browser_handler.exceptions.ElementNotInteractableException:
            like_buttons = None
        if like_buttons and len(like_buttons) > 1:
            like_buttons[0].send_keys(self.browser_handler.keys.ENTER)
            random.shuffle(like_buttons)
            like_button = random.choice(like_buttons)
            like_button.send_keys(self.browser_handler.keys.ENTER)
            time.sleep(5)

    def share_action(self):
        try:
            share_button = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.SHARE_BUTTON)
        except self.browser_handler.exceptions.NoSuchElementException:
            share_button = None
        if share_button:
            for _ in range(2):
                share_button.send_keys(self.browser_handler.keys.ENTER, self.browser_handler.keys.TAB)
                time.sleep(2)
            share_button.send_keys(self.browser_handler.keys.ENTER, self.browser_handler.keys.ENTER)

    def action_simulator(self):
        self.login()
        while True:
            self.browser_handler.scroll_page()
            if self.random_action():
                # self.share_action()
                self.like_action()
            time.sleep(5)

    def login(self):
        if self.logged_in_status:
            print(f"Logged in")
            return
        if not self.logged_in_status:
            print(f"Start login")
            login_with_cookies_status = True
            for _ in range(3):
                self.browser_handler.open_url(FacebookUrl.M_FACEBOOK_URL.format(""))
                time.sleep(10)
                login_with_cookies_status = self.login_with_cookies()
                if login_with_cookies_status:
                    break
            if not login_with_cookies_status:
                self.browser_handler.close_driver()
                raise ValueError("No alive cookies found")
            self.logged_in_status = True

    def login_with_cookies(self):
        print("login with cookies")
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.USERNAME_FORM], wait_time=30):
            raise HTTPError(f"{FacebookXPath.USERNAME_FORM} could not found before load cookie")
        load_cookie_status = self.browser_handler.load_cookie(
            xpath_list=[FacebookXPath.SEARCH_MOBILE_FORM], cookies=self.cookies)
        return load_cookie_status
