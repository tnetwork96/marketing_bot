import time
import random
from core.browser.browser_handler import BrowserHandler
from core.constant.base_selenium_constant import VietSchool, FacebookXPath


class ScoreCrawler(object):
    def __init__(self):
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option()

    def read_score(self, link, manager, school_name, sbd):
        print(f"opening link {link}")
        self.browser_handler.open_url(link)
        if not self.browser_handler.web_drive_wait_until(xpath_list=[VietSchool.XEM_PATTERN], wait_time=30):
            print(f"Can not load {link}")
            return
        # chon tinh
        self.chose_dropdown_list('[aria-labelledby="select2-cboDKTinh1-container"]',
                                 "select2-search__field", "Khánh Hòa")
        # chon so/phong
        self.chose_dropdown_list('[aria-labelledby="select2-cboDKHuyenID1-container"]',
                                 "select2-search__field", manager)
        # chon truong
        self.chose_dropdown_list('[aria-labelledby="select2-cboDKTruongID1-container"]',
                                 "select2-search__field", school_name)
        identifier_field = self.browser_handler.web_drive_wait(self.browser_handler.driver, 600).until(
            self.browser_handler.expected_conditions.presence_of_element_located(
                (self.browser_handler.by.ID, "txtSBD"))
        )
        time.sleep(1)
        identifier_field.send_keys(sbd)
        identifier_field.send_keys(self.browser_handler.keys.ENTER)
        time.sleep(1)
        xem_button = self.browser_handler.web_drive_wait(self.browser_handler.driver, 600).until(
            self.browser_handler.expected_conditions.presence_of_element_located(
                (self.browser_handler.by.ID, "btnFinds"))
        )
        xem_button.send_keys(self.browser_handler.keys.ENTER)
        time.sleep(2)
        # Find all rows in the table
        rows = self.browser_handler.driver.find_elements(self.browser_handler.by.XPATH, "//div[@class='wj-row']")
        # Loop through each row and extract data from each cell
        data_rows = list()
        for row in rows:
            cells = row.find_elements(self.browser_handler.by.CSS_SELECTOR, '[class^=wj-cell]')
            data = [cell.text for cell in cells]
            if data:
                try:
                    int(data[0])
                except ValueError:
                    continue
                data_rows.append(data)
        # self.browser_handler.close_driver()
        # print(data_rows)
        return data_rows

    def chose_dropdown_list(self, container, search_field_pattern, text):
        while True:
            dropdown_tinh = self.browser_handler.web_drive_wait(self.browser_handler.driver, 600).until(
                self.browser_handler.expected_conditions.presence_of_element_located((
                    self.browser_handler.by.CSS_SELECTOR, container))
            )
            try:
                dropdown_tinh.send_keys(self.browser_handler.keys.SPACE)
                break
            except self.browser_handler.exceptions.StaleElementReferenceException:
                time.sleep(2)
                print(f"retry find {container}")
                continue
        search_field = self.browser_handler.web_drive_wait(self.browser_handler.driver, 600).until(
            self.browser_handler.expected_conditions.presence_of_element_located(
                (self.browser_handler.by.CLASS_NAME, search_field_pattern))
        )
        time.sleep(1)
        search_field.send_keys(text)
        time.sleep(1)
        search_field.send_keys(self.browser_handler.keys.ENTER)
        time.sleep(1)

    def close(self):
        self.browser_handler.close_driver()