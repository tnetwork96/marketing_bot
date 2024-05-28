from time import time, sleep
from random import choice as random_choice, randint
from json.decoder import JSONDecodeError
from json import loads as json_loads
from json import dumps as json_dumps
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from core.util.file_handler import FileHandler
from core.constant.base_selenium_constant import BrowserOptionConstant, \
    CookieConstant, JSConstant, DriverPathConstant


class BrowserHandler(object):
    def __init__(self, browser_name):
        self.browser_name = browser_name
        self.web_drive_wait = WebDriverWait
        self.exceptions = exceptions
        self.keys = Keys
        self.expected_conditions = expected_conditions
        self.by = By
        self.driver_path = DriverPathConstant.CHROME_DRIVER
        self.driver_binary_path = DriverPathConstant.HEADLESS_CHROME
        self.driver = None
        self.cookie_file_name = "cookies_selenium.txt"
        self.cookies = None
        self.now = time()
        self.scroll_offset = 1

    def read_new_feed(self, time_interval):
        while True:
            if self.get_current_interval_time() >= time_interval:
                break
            self.scroll_page()

    def get_current_interval_time(self):
        return int(time() - self.now)

    def open_url(self, url: str):
        """Access url on browser"""
        self.driver.get(url)

    def restart_driver(self):
        """Close selenium driver and set option for selenium"""
        self.close_driver()
        self.set_driver_option()

    def close_driver(self):
        """Close selenium browser"""
        self.driver.close()
        self.driver.quit()

    def get_browser_option(self):
        options = None
        if self.browser_name == "firefox":
            options = webdriver.FirefoxOptions()
        elif self.browser_name == "chrome":
            options = webdriver.ChromeOptions()
        return options

    def get_browser_driver(self, options, profile_path):
        driver = None
        if self.browser_name == "firefox":
            profile_path = r"C:\Users\tnetw\AppData\Roaming\Mozilla\Firefox\Profiles\z7wp0gn5.default"
            profile = webdriver.FirefoxProfile(profile_path)

            driver = webdriver.Firefox(firefox_profile=profile, options=options)
            if profile_path:
                driver = webdriver.Firefox(options=options, firefox_profile=profile_path)
        elif self.browser_name == "chrome":
            driver = webdriver.Chrome(options=options)
            if profile_path:
                driver = webdriver.Chrome(options=options, chrome_options=profile_path)
        return driver

    def set_driver_option(self):
        """Set browser option"""
        options = webdriver.FirefoxOptions()
        profile_path = r"C:\Users\tnetw\AppData\Roaming\Mozilla\Firefox\Profiles\z129atq1.default-release"
        options.add_argument(f"--profile {profile_path}")
        windows_size_argument = self.get_browser_window_size_argument_from_cookie(self.get_cookie())
        if windows_size_argument:
            options.add_argument(windows_size_argument)
        # options.add_argument(BrowserOptionConstant.HEADLESS)
        options.add_argument(BrowserOptionConstant.NO_SANDBOX)
        options.add_argument(BrowserOptionConstant.SINGLE_PROCESS)
        options.add_argument(BrowserOptionConstant.DISABLE_DEV_SHM_USAGE)
        self.driver = webdriver.Firefox(options=options)
        sleep(20)

    @staticmethod
    def get_browser_window_size_argument_from_cookie(cookies):
        """Set screen size for selenium if cookies contain screen size info"""
        windows_size_argument = ""
        if not cookies:
            return windows_size_argument
        cookies = cookies.get(CookieConstant.COOKIE) if CookieConstant.COOKIE in cookies else cookies
        for cookie in cookies:
            if cookie.get(CookieConstant.NAME) == CookieConstant.WD:
                wd_info = cookie[CookieConstant.VALUE]
                width, height = wd_info.strip().lower().split("x")
                windows_size_argument = BrowserOptionConstant.WINDOWS_SIZE.format(width, height)
                break
        return windows_size_argument

    def get_page_source(self):
        """Get source html"""
        return self.driver.page_source

    def get_user_agent(self):
        return self.driver.execute_script("return navigator.userAgent")

    def scroll_page(self, scroll_times: int = 1):
        """Scroll page by execute javascript"""
        scroll_offset = 0
        print("scroll_times: ", scroll_times)
        for _ in range(scroll_times):
            length = randint(300, 700)
            length = random_choice([length * -1, length])
            self.driver.execute_script(JSConstant.WINDOW_SCROLL_TO.format(scroll_offset, scroll_offset + length))
            scroll_offset += length
            sleep(randint(60, 500))

    def load_cookie(self, xpath_list: list, wait_time: int = 10, cookies=None):
        """
        - Get all cookies and sort cookies by last_time_request
        """
        self.cookies = self.get_cookie(cookies)
        self.driver.delete_all_cookies()

        [self.driver.add_cookie(cookie) for cookie in self.remove_cookie_properties_un_use(self.cookies)]
        self.driver.refresh()
        load_cookie_status = self.web_drive_wait_until(xpath_list, wait_time)
        self.save_cookie()
        return load_cookie_status

    def save_cookie(self):
        if self.cookies:
            FileHandler.write_file(self.cookie_file_name, json_dumps(self.cookies), override=True)
            return json_dumps(self.cookies)

    def get_cookie(self, cookies=None):
        raw_cookie = FileHandler.read_file(self.cookie_file_name) if not cookies else cookies
        try:
            cookies = json_loads(raw_cookie)
        except JSONDecodeError:
            cookies = ""
        return cookies

    def get_driver_cookie(self):
        return self.driver.get_cookies()

    def web_drive_wait_until(self, xpath_list: list, wait_time: int = 10):
        """wait html pattern loading"""
        for xpath in xpath_list:
            try:
                self.web_drive_wait(self.driver, wait_time).until(
                    self.expected_conditions.presence_of_element_located(
                        (self.by.XPATH, xpath)))
                return xpath
            except (self.exceptions.NoSuchElementException,
                    self.exceptions.TimeoutException):
                continue
        return None

    @staticmethod
    def remove_cookie_properties_un_use(cookies):
        """Remove un-use cookies properties"""
        for cookie in cookies:
            if CookieConstant.EXPIRY in cookie:
                del cookie[CookieConstant.EXPIRY]
            if CookieConstant.SAME_SITE in cookie:
                del cookie[CookieConstant.SAME_SITE]
        return cookies
