from time import sleep
from telegram import Bot
from script_kiddies.dmcl.dienmaycholon_price import DMCLPrice
from core.google_api.google_sheet_handler import GoogleSheetHandler

TOKEN = "5675446466:AAEBBUGxuUunLuyy4sI6Y6sv62obNJeaIdE"
GROUP_CHAT_ID = "-821149273"
gg_sheet_handler = GoogleSheetHandler("GROUPS_MANAGER")
spreadsheet_name = "Dien May Cho Lon"

def send_message(chat_id, text):
    bot = Bot(TOKEN)
    bot.send_message(chat_id=chat_id, text=text)
def iterate_product():
    key_words = gg_sheet_handler.read(spreadsheet_name, "key_word")
    sale_percents = gg_sheet_handler.read(spreadsheet_name, "sale_percent")
    for kw, perc in zip(key_words, sale_percents):
        print(f"{kw} sale {perc} %")
        dmcl_price = DMCLPrice(kw)
        page = None
        while True:
            rs = dmcl_price.result_search(page=page)
            list_product = rs["data"]["hits"]["hits"]
            for prod in list_product:
                data = dmcl_price.parse_product(prod)
                yield  dmcl_price, data, kw, perc
            try:
                page = dmcl_price.get_page(list_product[-1])
            except IndexError:
                break
            sleep(15)

product_list = iterate_product()

for dmcl, prod, kw, sale_percent in product_list:
    if prod['discount_percent'] > int(sale_percent):
        link_product = f"https://dienmaycholon.vn/{prod['cate_alias']}/{prod['alias']}"
        in_stock, in_stock_status = dmcl.check_stock_with_selenium(link_product)
        if u"hàng sắp về" in in_stock_status:
            gg_sheet_handler.write(spreadsheet_name, "hang sap ve", link_product)
            print(link_product, in_stock, in_stock_status)
        if in_stock:
            text = f"""\n
            - giá bán: {prod['saleprice']}
            - giá khuyến mãi: {prod['discount']}
            - % giảm: {prod['discount_percent']}
            - tên: {prod['name']}
            - link: {link_product}
            - in stock: {in_stock}
            """
            send_message(GROUP_CHAT_ID, text)
            sleep(5)