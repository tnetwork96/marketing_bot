import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core.constant.request import Request


class GoogleSheetHandler:
    """Class handler read and write data to google sheet"""

    def __init__(self, sheet_name: str):
        super().__init__()
        self.sheet_name = sheet_name
        self.credential_file = "mmoreport.json"
        self.credential = ServiceAccountCredentials.from_json_keyfile_name(self.credential_file, Request.SCOPE)
        self.client = gspread.authorize(self.credential)
        self.sheet = self.client.open(self.sheet_name)

    def read(self, spread_sheet_name: str, field_name: str):
        """Read data from Google Sheet"""
        field_value = []
        sheet = self.sheet.worksheet(spread_sheet_name)
        rows = sheet.get_all_values()
        header_rows = [x for x in rows[0] if x.strip()]
        rows.pop(0)
        try:
            bot_index = header_rows.index(field_name)
        except ValueError:
            bot_index = None
        if bot_index is not None and rows:
            for idx, row in enumerate(rows):
                field_value.append(row[bot_index])
        return [x for x in field_value if x.strip()]

    def read_all(self, spread_sheet_name: str):
        """Read data from Google Sheet"""
        sheet = self.sheet.worksheet(spread_sheet_name)
        rows = sheet.get_all_values()
        return rows

    def write(self, spread_sheet_name: str, field_name: str, row_value: str):
        """Write to google"""
        sheet = self.sheet.worksheet(spread_sheet_name)
        rows = sheet.get_all_values()
        header_rows = [x for x in rows[0] if x.strip()]
        rows.pop(0)
        try:
            bot_index = header_rows.index(field_name)
        except ValueError:
            bot_index = None
        if bot_index is not None and rows:
            for idx, row in enumerate(rows):
                if row[bot_index] == "":
                    sheet.update_cell(idx + 2, bot_index + 1, row_value)
                    return
            sheet.update_cell(len(rows) + 2, bot_index + 1, row_value)
        else:
            sheet.update_cell(len(rows) + 2, bot_index + 1, row_value)

    def over_write(self, spread_sheet_name: str, field_name: str, row_value: str):
        """Write to google"""
        sheet = self.sheet.worksheet(spread_sheet_name)
        rows = sheet.get_all_values()
        header_rows = [x for x in rows[0] if x.strip()]
        rows.pop(0)
        try:
            bot_index = header_rows.index(field_name)
        except ValueError:
            bot_index = None
        if bot_index:
            sheet.update_cell(2, bot_index + 1, row_value)

#     def get_bot_have_not_comment(self, spread_sheet_name, newest_post_link):
#         sheet = self.sheet.worksheet(spread_sheet_name)
#         rows = sheet.get_all_values()
#         title_rows = rows[0].copy()
#         bot_have_not_comment_list = rows[0].copy()
#         rows.pop(0)
#         for row_values in rows:
#             for value_idx, link in enumerate(row_values):
#                 try:
#                     bot_name = title_rows[value_idx]
#                 except IndexError:
#                     continue
#                 if link == newest_post_link:
#                     bot_have_not_comment_list.remove(bot_name)
#         return bot_have_not_comment_list
#
#

# a = GoogleSheetHandler("GROUPS_MANAGER").read("total bot", "count")
# print("post link used: ", a)
# GoogleSheetHandler("GROUPS_MANAGER").over_write("total bot", "count", 20)
# a = GoogleSheetHandler("GROUPS_MANAGER").write("post link used", "phamthungan", "asdsad")
# post_link = "https://www.facebook.com/groups/reviewdulichnhatrang79/permalink/3211675069075004/?fs=e&s=cl"
# all_value = GoogleSheetHandler("GROUPS_MANAGER").read_all("post link used")
# all_bot = len(all_value[0])
#
# post_link_commented_count = len([v for value in all_value[1:] for v in value if post_link in v])
# print(post_link_commented_count)
# print(all_bot - post_link_commented_count)