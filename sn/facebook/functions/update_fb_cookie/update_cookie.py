import time
from random import choice
from requests import HTTPError
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import FacebookUrl, FacebookXPath



class UpdateCookie(object):
    def __init__(self, cookies):
        self.cookies = cookies
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option(reduce_cpu=True, cookies=cookies)
        self.recv_sms_status = False

    def login_with_cookies(self):
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.USERNAME_FORM], wait_time=30):
            raise HTTPError(f"{FacebookXPath.USERNAME_FORM} could not found before load cookie")
        load_cookie_status = self.browser_handler.load_cookie(xpath_list=[FacebookXPath.SEARCH_MOBILE_FORM,
                                                                          FacebookXPath.WHAT_ON_YOUR_MIND],
                                                              cookies=self.cookies)
        return load_cookie_status

    def login(self):
        print("login with cookies: ", self.cookies)
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

    def request_friend(self, username):
        link = FacebookUrl.FACEBOOK_URL.format(username)
        # ADD_FRIEND_PATTERN
        self.browser_handler.open_url(link)
        if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.ADD_FRIEND_BUTTON],
                                                         wait_time=10):
            add_friend_button = self.browser_handler.driver.\
                find_element_by_xpath(FacebookXPath.ADD_FRIEND_BUTTON)
            add_friend_button.send_keys(self.browser_handler.keys.SPACE)
            if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.ADD_FRIEND_WARNING],
                                                         wait_time=10):
                add_friend_warning = self.browser_handler.driver.\
                    find_element_by_xpath(FacebookXPath.ADD_FRIEND_WARNING)
                time.sleep(1)
                add_friend_warning.send_keys(self.browser_handler.keys.TAB)
                time.sleep(1)
                add_friend_warning.send_keys(self.browser_handler.keys.TAB)
    def check_friends_request(self):
        self.browser_handler.open_url("https://www.facebook.com/friends")
        if self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.FRIEND_REQUEST_PATTERN],
                                                         wait_time=10):
            try:
                confirm_button = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.CONFIRM_BUTTON)
            except self.browser_handler.exceptions.NoSuchElementException:
                return
            confirm_button.send_keys(self.browser_handler.keys.SPACE)


    def chat_random(self, message):
        self.browser_handler.open_url("https://www.facebook.com/messages/t")
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.SEARCH_MESSENGER_PATTERN],
                                                         wait_time=10):
            return
        time.sleep(2)
        element = self.browser_handler.driver.find_element_by_xpath("//body")
        time.sleep(2)
        [element.send_keys(char) for char in message]
        time.sleep(2)
        element.send_keys(self.browser_handler.keys.ENTER)

    def update_new_cookie(self):
        if not self.logged_in_status:
            self.login()
        # self.chat_random(choice(message_list))
        # time.sleep(10)
        # self.check_friends_request()
        link = FacebookUrl.FACEBOOK_URL.format("")
        self.browser_handler.open_url(link)
        print("user-agent: ", self.browser_handler.get_user_agent())
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.SEARCH_FORM,
                                                                    FacebookXPath.FRIEND_PATTERN,
                                                                     FacebookXPath.CONTACT_PATTERN],
                                                         wait_time=10):
            return
        self.browser_handler.scroll_page(choice([3, 10]))
        self.browser_handler.save_cookie()
        cookie = self.browser_handler.get_cookie()
        self.browser_handler.close_driver()
        return cookie
    def verify_phone(self, wait=False):
        if not self.logged_in_status:
            self.login()
        time.sleep(5)
        self.browser_handler.open_url("https://business.facebook.com/business_locations/")
        print("user-agent: ", self.browser_handler.get_user_agent())
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.ENTER_CODE],
                                                 wait_time=10):
            return
        self.browser_handler.close_driver()
        # if wait:
        #     while True:
        #         if self.recv_sms_status:
        #             # self.browser_handler.close_driver()
        #             break
        #         time.sleep(30)

    def fill_verify_sms(self, sms):
        verify_status = False
        if not self.logged_in_status:
            self.login()
        time.sleep(5)
        self.browser_handler.open_url("https://business.facebook.com/business_locations/")
        print("user-agent: ", self.browser_handler.get_user_agent())
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.ENTER_CODE],
                                                 wait_time=30):
            verify_status = True
            return verify_status
        if not sms:
            return verify_status
        element = self.browser_handler.driver.find_element_by_xpath(FacebookXPath.ENTER_CODE)
        time.sleep(2)
        [element.send_keys(char) for char in sms]
        time.sleep(2)
        element.send_keys(self.browser_handler.keys.TAB)
        time.sleep(5)
        element.send_keys(self.browser_handler.keys.TAB)
        time.sleep(5)
        element.send_keys(self.browser_handler.keys.ENTER)
        if not self.browser_handler.web_drive_wait_until(xpath_list=[FacebookXPath.ENTER_CODE],
                                                 wait_time=30):
            verify_status = True
        return verify_status


    def check_still_verify(self, sms):
        try:
            int(sms)
            # self.recv_sms_status = True
            return sms
        except TypeError:
            return ""

