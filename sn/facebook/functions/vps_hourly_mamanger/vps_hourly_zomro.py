import time
from requests import HTTPError
import random
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import OpNet


class VpsZomRo(object):
    def __init__(self, cookies=None):
        self.cookies_file_name = "cookies_selenium.txt"
        self.cookies = cookies
        self.logged_in_status = False
        self.join_chat_room = False
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option()
        self.driver = self.browser_handler.driver

    def create_vps(self):
        self.browser_handler.open_url("https://panel.op-net.com/onecloud/new")
        keys = self.browser_handler.keys
        by = self.browser_handler.by
        if not self.browser_handler.web_drive_wait_until(xpath_list=[OpNet.shop_now_label], wait_time=180):
            return
        time.sleep(5)
        element = self.driver.find_element_by_css_selector("input[data-cpu='1'][data-memory='1024']")
        # Sử dụng JavaScript để click vào phần tử
        self.driver.execute_script("arguments[0].click();", element)

    # def order(self):
    #     self.browser_handler.open_url("https://cp.zomro.com/services/cloud_vps")
    #     time.sleep(30)
    #     keys = self.browser_handler.keys
    #     by = self.browser_handler.by
    #     if not self.browser_handler.web_drive_wait_until(xpath_list=[ZomRo.ORDER_BUTTON], wait_time=180):
    #         return
    #     js_code = """
    #     var links = document.querySelectorAll("a[id^='instanceManageLink-']");
    #     links.forEach(function(link) {
    #         console.log('Clicking on link with text: ' + link.textContent + ' and id: ' + link.id);
    #         link.click();
    #     });
    #     """
    #     self.driver.execute_script(js_code)


vps = VpsZomRo()
vps.create_vps()
