import time
from requests import HTTPError
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import FacebookUrl, FacebookXPath
from core.mongodb.mongo_connection import MongoConnection


# from core.google_api.google_sheet_handler import GoogleSheetHandler


class member_collector(object):
    def __init__(self, city=None, region=None, sector=None):
        self.cookies_file_name = "cookies_selenium.txt"
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler()
        self.browser_handler.set_driver_option()
        self.city = city
        self.region = region
        self.sector = sector

    def collect_data(self, group_link):
        if not self.logged_in_status:
            self.login()
        self.browser_handler.open_url(FacebookUrl.FACEBOOK_MEMBERS_NEAR_U_URL.strip().format(group_link))
        # if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.FIND_MEMBERS_PATTERN, wait_time=30):
        #     print("Load members url fail")
        #     return
        time.sleep(15)
        user_list = []
        count = 0
        flag = False
        while True:
            temp = []
            member_list = self.browser_handler.driver.find_elements_by_xpath(FacebookXPath.LINK_PATTERN)
            for member in member_list:
                link = member.get_attribute('href')
                if "/user/" in link:
                    if count > 30:
                        flag = True
                        break
                    temp.append(link)
                    temp = list(set(temp))
            if len(set(temp) & set(user_list)) == len(temp):
                self.browser_handler.scroll_page()
                time.sleep(5)
                count += 1
                print(f"trung lan {count}")
                # print(f"list trung`: {set(temp) & set(user_list)}")
            else:
                count = 0
            users_extra = self.get_extra_elements(temp, user_list)
            self.update_user_to_db(users_extra)
            user_list.extend(users_extra)
            if flag:
                break
            time.sleep(10)
        user_list = list(set(user_list))
        print(f"num members: {len(user_list)}")

    def get_extra_elements(self, f_list, s_list):
        f_set = set(f_list)
        s_set = set(s_list)
        return list(f_set - s_set if len(f_set) > len(s_set) else s_set - f_set)

    def update_user_to_db(self, user_list):
        mongo_connection = MongoConnection()
        mongo_connection.init_connection("facebook")
        for user in user_list:
            element_split = user.split("/user/")
            user_id = element_split[-1].strip("/")
            group_id = element_split[0].split("groups/")[-1]
            mongo_connection.upsert("users", condition={"user_id": user_id, "sector": self.sector},
                                    documents={"user_id": user_id,
                                               "city": self.city,
                                               "region":  self.region,
                                               "sector": self.sector,
                                               "group_id": group_id,
                                               "time": time.time()
                                               })
        mongo_connection.mongo_client.close()

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
        if not self.browser_handler.web_drive_wait_until(xpath=FacebookXPath.USERNAME_FORM, wait_time=30):
            raise HTTPError(f"{FacebookXPath.USERNAME_FORM} could not found before load cookie")
        load_cookie_status = self.browser_handler.load_cookie(xpath=FacebookXPath.SEARCH_MOBILE_FORM)
        return load_cookie_status
