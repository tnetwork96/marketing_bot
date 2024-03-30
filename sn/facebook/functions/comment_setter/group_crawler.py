import random
from re import sub as re_sub
from json import loads as json_loads
from core.constant.base_facebook import Request
from core.request_handler.base_request_handler import BaseRequestHandler
from core.constant.base_selenium_constant import CookieConstant

request_handler = BaseRequestHandler()


class GroupCrawler(object):
    def __init__(self):
        self.group_link_file_name = "group_post_link.txt"
        self.cookies_file_name = "cookies.txt"
        self.logged_in_status = False
        self.acc_via = None
        self.credential_mapping = self.get_credential_info()

    def collect_data(self, group_id=None):
        response_obj = self.make_request_api(group_id)
        if response_obj.status_code != 200:
            yield response_obj, ""
        group_posts = response_obj.json()
        post_relevant_list = []
        for post in group_posts.get("data", []):
            if not post.get("message"):
                continue
            post_relevant_list.append(post)
        if not post_relevant_list:
            return post_relevant_list
        latest_posts = sorted(post_relevant_list, key=lambda x: x["created_time"], reverse=True)
        for latest_post in latest_posts:
            message = f'{latest_post["message"]}'
            link = latest_post["actions"][0]["link"]
            link_exist = self.add_link(link)
            if not link_exist:
                message_body = message[:150]
                message_body = re_sub(r"([_*\[\]()~`>\#\+\-=|\.!{}])", r"\\\1", message_body)
                message_body = message_body.replace('%', '\\%25')
                message_body = message_body.replace('#', '\\%23')
                message_body = message_body.replace('+', '\\%2B')
                message_body = message_body.replace('*', '\\%2A')
                message_body = message_body.replace('&', '\\%26')
                message_body = message_body + "\nLink: " + link
                yield response_obj, message_body
            else:
                print("da co link roi")

    def get_credential_info(self):
        with open(self.cookies_file_name, "r") as f:
            data = json_loads(f.read().strip())
        id_list = [x for x in data]
        for user_id in id_list:
            if isinstance(data[user_id][CookieConstant.COOKIE], list):
                new_cookie = self.convert_cookies(data[user_id][CookieConstant.COOKIE])
                data[user_id][CookieConstant.COOKIE] = new_cookie
        return data

    @staticmethod
    def convert_cookies(cookies):
        cookies_update = {}
        for ele in cookies:
            cookies_update.update({ele['name']: ele['value']})
        return cookies_update

    @staticmethod
    def convert_message(message_body):
        message_body = re_sub(r"([_*\[\]()~`>\#\+\-=|\.!{}])", r"\\\1", message_body)
        message_body = message_body.replace('%', '\\%25')
        message_body = message_body.replace('#', '\\%23')
        message_body = message_body.replace('+', '\\%2B')
        message_body = message_body.replace('*', '\\%2A')
        message_body = message_body.replace('&', '\\%26')
        return message_body

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

    # def save_cookies(self, social_id, response_obj):
    #     response_cookie = response_obj.cookies
    #     for key in response_cookie:
    #         if key in self.credential_mapping[str(social_id)]["cookie"]:
    #             self.credential_mapping[str(social_id)]["cookie"]

    def make_request_api(self, social_id):
        credential = self.random_acc_via()
        token = credential["token"]
        cookie = credential[CookieConstant.COOKIE]
        post_request_url = Request.POST_URL.format(social_id, Request.LIMIT, token)
        response_obj = request_handler.make_request(url=post_request_url, cookies=cookie)
        return response_obj

    def random_acc_via(self):
        via_user_id = random.choice([x for x in self.credential_mapping])
        return self.credential_mapping[via_user_id]
