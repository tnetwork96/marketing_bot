import os
import random
import re
import subprocess
import docker
import time
from core.google_api.google_sheet_handler import GoogleSheetHandler

gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
spreadsheet_name = "new post link"


# def get_bot_have_not_comment(newest_post_link):
#     sheet = gg_sheet_handler.sheet.worksheet(spreadsheet_name)
#     rows = sheet.get_all_values()
#     title_rows = rows[0].copy()
#     bot_have_not_comment_list = rows[0].copy()
#     rows.pop(0)
#     for row_values in rows:
#         for value_idx, link in enumerate(row_values):
#             try:
#                 bot_name = title_rows[value_idx]
#             except IndexError:
#                 continue
#             if link == newest_post_link:
#                 bot_have_not_comment_list.remove(bot_name)
#     return bot_have_not_comment_list

def get_client_info(client_name, clients):
    for client_info in clients:
        if client_info.name == client_name:
            return cli


while True:
    client = docker.from_env()
    client_list = client.containers.list(all=True)
    for cli in client_list:
        if cli.status == "exited" and \
                "seafootbot" not in cli.name:
            print("bot name: ", cli.name, cli.status)
            os.system(f'sudo docker start {cli.name}')
            time.sleep(10)
            p = subprocess.Popen(f'sudo docker ps', stdout=subprocess.PIPE, shell=True)
            console_text = list(p.communicate())[0].decode("utf-8")
            containers = [x for x in console_text.split("\n") if x.strip()][1:]
            bot_services = [c for c in containers if "seafootbot" not in c]
            if len(bot_services) > 0:
                wait_time = random.choice(range(6*60, 10*60))
                print(f"da co bot chay, sleep {wait_time}s")
                time.sleep(wait_time)
            time.sleep(5)
    time.sleep(30)
