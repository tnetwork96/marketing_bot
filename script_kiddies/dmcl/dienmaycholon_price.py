import time
from json import loads
from requests import session
from urllib.parse import quote
from bs4 import BeautifulSoup
from core.browser.browser_handler import BrowserHandler

# timestamp =

s = session()
header = {
    "Host": "dienmaycholon.vn",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://dienmaycholon.vn/tu-khoa/quat",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


class DMCLPrice:
    def __init__(self, key_word):
        self.key_word = quote(key_word)
        self.browser_handler = BrowserHandler("firefox")
        self.browser_handler.set_driver_option(reduce_cpu=True)
        self.url_dmcl_product_result = "https://dienmaycholon.vn/api/product/result"
    def side_bar(self):
        rs = s.get(url=f"https://dienmaycholon.vn/api/product/sidebar?k={self.key_word}&tag={self.key_word}",
                   headers=header)
        return loads(rs.text)
    def result_search(self, page=None):
        slide_bar_data = self.side_bar()
        cid_cate = slide_bar_data["data"]["cid_cate"]
        offset = 15
        if not page:
            url = f"{self.url_dmcl_product_result}?k={self.key_word}&cid_cate=" \
                  f"{cid_cate}&offset={offset}"
        else:
            url = f"{self.url_dmcl_product_result}?k={self.key_word}&cid_cate=" \
                  f"{cid_cate}&page={page}" \
                  f"&offset={offset}"
        rs = s.get(url=url, headers=header)
        return loads(rs.text)
    def parse_product(self, product_data):
        src = product_data["_source"]
        _sort = product_data["sort"]
        _name = src["name"]
        _id = product_data["_id"]
        _picture = src["picture"]
        _cate_alias = src["cate_alias"]
        _alias = src["alias"]
        _saleprice = int(src["saleprice"])
        _discount = int(src["discount"])
        image = f"https://cdn01.dienmaycholon.vn/filewebdmclnew/" \
                f"DMCL21/Picture//Apro/Apro_product_{_id}/{_picture}_450.png.webp"
        _discount_percent = ((_saleprice - _discount) / _saleprice) * 100
        return dict(sort=_sort, name=_name,
                    id=_id, picture=_picture,
                    image=image, saleprice=_saleprice,
                    discount=_discount, discount_percent=round(_discount_percent),
                    cate_alias=_cate_alias, alias=_alias)

    def get_page(self, product):
        return ",".join([str(x) for x in self.parse_product(product)["sort"]])

    def open_product_link(self, url):
        self.browser_handler.open_url(url)
        self.browser_handler.web_drive_wait_until(xpath_list=["//strong[@id='conhang']"], wait_time=10)
        source = self.browser_handler.driver.page_source
        return source

    def check_stock_with_selenium(self, url):
        in_stock = False
        in_stock_status = ""
        source = self.open_product_link(url)
        time.sleep(3)
        soup = BeautifulSoup(source, "html.parser")
        element = soup.find(id="conhang")
        if not element:
            print("error url: ", url)
        if element:
            text = element.text.lower()
            in_stock_status = text
            if u"còn hàng" in text:
                in_stock = True
        return in_stock, in_stock_status