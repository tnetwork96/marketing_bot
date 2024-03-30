import time
from random import choice, shuffle, randint
from bs4 import BeautifulSoup
from json import loads as json_loads
from core.browser.browser_handler import BrowserHandler
from threading import Event, Thread
from re import search

event = Event()


class UserSimulator(object):
    def __init__(self):
        self.logged_in_status = False
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option()

    def access_url(self, url):
        self.browser_handler.open_url(url)

    def play_videos(self):
        # lay danh sach video tu gg sheet
        video_list = ["hongkong1", "tinh yeu mau nang",
                      "sai gon bao nhieu den do",
                      "phia nha khong nang", "mua",
                      "yeu xa", "di vang cuoc tinmh"]
        shuffle(video_list)
        print(video_list)
        for video_name in video_list:
            self.play_video(video_name)

            video_duration = self.get_video_duration()
            sleep_time = randint(choice([int(video_duration/2), int(video_duration/3)]), video_duration)
            sleep_time = int(sleep_time / 1000)
            print(f"watch video in {sleep_time} seconds")
            time.sleep(sleep_time)

    def play_video(self, video_title):
        search_input = self.browser_handler.driver.find_element_by_css_selector('input#search[name="search_query"]')
        time.sleep(5)
        search_input.send_keys(video_title)
        time.sleep(2)
        search_input.send_keys(self.browser_handler.keys.ENTER)
        time.sleep(5)
        html_content = self.browser_handler.get_page_source()
        soup = BeautifulSoup(html_content, 'html.parser')
        video_name = soup.find_all('a', id='video-title')[0]
        href = video_name['href']
        self.browser_handler.open_url(f"https://www.youtube.com{href}")
        if self.browser_handler.web_drive_wait_until(xpath_list=["//button[@id='avatar-btn']"],
                                                     wait_time=30):
            time.sleep(3)
            should_view_comments = choice([True, False] * 5)
            if should_view_comments:
                self.view_comments(back_video=True)
            print("play")
            time.sleep(2)
            webpage = self.browser_handler.driver.find_element_by_tag_name("body")
            webpage.send_keys(self.browser_handler.keys.SPACE)

    def view_comments(self, back_video=False):
        print("view comments")
        scroll_offset_list = self.browser_handler.scroll_page(choice([5, 10]))
        time.sleep(randint(3, 5))
        if not back_video:
            return
        print("back video")
        self.browser_handler.scroll_page_reverse(scroll_offset_list)
        time.sleep(randint(3, 5))

    def get_video_duration(self):
        html_text = self.browser_handler.driver.page_source
        match = search(r'"approxDurationMs":"(\d+)"', html_text)
        if match:
            approx_duration_ms = match.group(1)
            approx_duration_ms_number = int(approx_duration_ms)
            # minute = self.seconds_to_minutes(approx_duration_ms_number)
            # print("video dai: ", minute)
            return approx_duration_ms_number

    def seconds_to_minutes(self, seconds):
        minutes = seconds // 60  # Số phút là phần nguyên khi chia cho 60
        # remaining_seconds = seconds % 60  # Số giây còn lại sau khi chuyển thành phút
        return minutes