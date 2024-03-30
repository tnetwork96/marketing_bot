import random
import sys
import time
from json import dumps
from os.path import exists
from core.constant.base_facebook import Request
from core.util.file_handler import FileHandler
from requests import session
from sn.facebook.functions.user_simulator.simulator import simulator
from core.google_api.google_sheet_handler import GoogleSheetHandler

gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
request = session()

# get_comment_url = f'http://{Request.API_SERVICE}/comments/get_comment'
get_comment_url = f'http://192.168.1.6:8000/comments/get_comment'
# remove_comment_url = f'http://{Request.API_SERVICE}/comments/remove_comment'
remove_comment_url = f'http://192.168.1.6:8000/comments/remove_comment'
# register_slot_url = f'http://{Request.API_SERVICE}/slot/register'
register_slot_url = f'http://192.168.1.6:8000/slot/register'
file_name = "post_link.txt"
ban_gr_file = "ban_group.txt"
spreadsheet_name = "post link used"
cookies_spreadsheet_name = "FB Cookies"
file_exists = exists(file_name)
if not file_exists:
    f = open(file_name, "w")
    f.close()


def get_old_post_links():
    return FileHandler.read_file(file_name).split("\n")


def check_link_exists(new_post_link, old_post_links):
    new_post_link = new_post_link.strip()
    for old_post_link in old_post_links:
        if old_post_link in new_post_link or old_post_link == new_post_link or new_post_link in old_post_link:
            return True
    return False


def remove_comment(post_link, comment):
    request.post(url=remove_comment_url, json={
        "comment": comment,
        "post_link": post_link
    })


def parse_group_id(group_link):
    """https://www.facebook.com/groups/nhatrang.bandoanuong/permalink/1156422051637937/"""
    elements = group_link.split("/groups/")[-1].split("/")
    return elements[0]


def save_cookies(cookies):
    gg_sheet_handler.over_write(cookies_spreadsheet_name, sys.argv[1].strip(), dumps(cookies))


def run_simulator():
    post_links_from_gg_api = gg_sheet_handler.read(spreadsheet_name, sys.argv[1].strip())
    group_dont_comment = [x.strip() for x in post_links_from_gg_api if "http" not in x.strip()]
    post_links = [x.strip() for x in post_links_from_gg_api if "http" in x.strip()]
    """Giãn thời gian request google api """
    time.sleep(15)
    data = request.post(url=get_comment_url, json={
        "post_link_list": post_links
    }).json().get("data", {})
    cookies = gg_sheet_handler.read(cookies_spreadsheet_name, sys.argv[1].strip())[0].strip()
    test = simulator(cookies=cookies)
    if not data:
        read_new_feed_times = random.randint(5, 13)
        print("read_new_feed_times: ", read_new_feed_times)
        test.read_new_feed()
        for _ in range(read_new_feed_times):
            print("reading new feed  ....")
            data = request.post(url=get_comment_url, json={
                "post_link_list": post_links
            }).json().get("data", {})
            if not data:
                test.read_new_feed(read_continue=True)
            else:
                print("Have comment")
                break

    if data:
        post_link = data.get("post_link")
        if post_link:
            post_link = post_link.strip()
        else:
            return
        group_id = parse_group_id(post_link)
        try:
            group_ban_list = FileHandler.read_file(ban_gr_file).split("\n")
        except FileNotFoundError:
            group_ban_list = []
        if group_id in group_ban_list:
            print("group nay block roi")
            return
        if check_link_exists(post_link, post_links):
            return
        for group_id in group_dont_comment:
            if group_id in post_link:
                print("khong duoc comment group nay")
                return
        comment = data.get("comment")
        group_action = test.comment_on_post(post_link, comment)
        save_cookies(test.browser_handler.get_driver_cookie())
        time.sleep(15)
        if group_action == "banned":
            FileHandler.write_file(ban_gr_file, group_id)
            gg_sheet_handler.write(spreadsheet_name, sys.argv[1].strip(), post_link)
            test.browser_handler.save_cookie()
            test.browser_handler.close_driver()
            return
        if group_action == "deleted":
            remove_comment(post_link, comment)
            gg_sheet_handler.write(spreadsheet_name, sys.argv[1].strip(), post_link)
            test.browser_handler.save_cookie()
            test.browser_handler.close_driver()
            return
        # neu comment thanh cong moi ghi vo file
        if post_link not in post_links:
            remove_comment(post_link, comment)
            gg_sheet_handler.write(spreadsheet_name, sys.argv[1].strip(), post_link)
        # test.like_action()
    test.browser_handler.close_driver()


run_simulator()
