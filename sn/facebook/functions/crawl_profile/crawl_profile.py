import time
from requests import HTTPError
from core.browser.browser_handler import BrowserHandler
from sn.facebook.functions.crawl_profile.profile_parser import ProfileParser
from core.constant.base_selenium_constant import FacebookUrl, FacebookXPath


class ProfileCrawler(object):
    def __init__(self):
        self.cookies_file_name = "cookies_selenium.txt"
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler("chrome")
        self.profile_parser = ProfileParser()
        self.browser_handler.set_driver_option(reduce_cpu=True)

    def login_with_cookies(self):
        print("login with cookies")
        if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.USERNAME_FORM, wait_time=30):
            raise HTTPError(f"{FacebookXPath.USERNAME_FORM} could not found before load cookie")
        load_cookie_status = self.browser_handler.load_cookie(xpath=FacebookXPath.SEARCH_MOBILE_FORM)
        return load_cookie_status

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

    def get_profile_data(self, username):
        if not self.logged_in_status:
            self.login()
        link = FacebookUrl.FACEBOOK_URL.format(username)
        self.browser_handler.open_url(link)
        if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.INTRO_PATTERN, wait_time=10):
            return
        # self.browser_handler.scroll_page(3)
        # element = self.browser_handler.driver.find_element_by_xpath("//body")
        # element.send_keys("j")
        html_text = self.browser_handler.get_page_source()
        intro_data = self.profile_parser.parse_intro(html_text)
        avatar_data = self.profile_parser.parse_avatar(html_text)
        # photos_data = self.profile_parser.parse_photos(self.browser_handler.get_page_source())
        print("intro_data: ", intro_data)
        print("avatar_data: ", avatar_data)
        profile_data = {"intro": intro_data["data"], "avatar": avatar_data}
        return dict(data=profile_data)

    def fake_behaviour(self):
        self.browser_handler.open_url(FacebookUrl.FACEBOOK_URL)
        if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.FRIEND_PATTERN, wait_time=10):
            return
        self.browser_handler.scroll_page(10)

# a = ProfileCrawler()
# data = a.get_profile_data(username="100011289941300")
# print("data: ", data)