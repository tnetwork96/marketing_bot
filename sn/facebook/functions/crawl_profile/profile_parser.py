import re
from bs4 import BeautifulSoup
class ProfileParser(object):
    def __init__(self):
        self.bs = BeautifulSoup
    def check_accept_char(self, string):
        temp = [c for c in string if not c.isalnum()]
        filter_temp = [x for x in temp if x not in ["/", "-", ",", ".", "(", ")"] and x.strip()]
        return False if len(filter_temp) > 0 else True

    def correct_intro(self, string_list, replace_pattern):
        if not string_list:
            return
        for string in string_list:
            if r"\u" in string:
                print("string: ", string)
                try:
                    string = string.encode('utf-8').decode('unicode-escape')
                except UnicodeDecodeError:
                    continue
                print("string after: ", string)
            if self.check_accept_char(string):
                print("string ok: ", string)
                return string.replace(replace_pattern, "").strip()

    def parse_intro_detail(self, html_text, pattern):
        pattern_rs = [x.strip().replace("\"", "")
                      for x in re.findall(f'{pattern} .*?\"', html_text)]

        if not pattern_rs:
            pattern_rs = [x.strip().replace("<", "")
                          for x in re.findall(f'{pattern} .*?\<', html_text)]
        print(pattern_rs)
        if pattern_rs:
            temp = self.correct_intro(pattern_rs, pattern)
            if temp:
                return temp
    def parse_intro(self, html_text):
        data = {}

        intro_item_list = ["Went to", "Worked at", "Studied at", "Lives in", "Works at", "From",
                           "Co-Founder / Partner at", "Manager at"]
        for intro_item in intro_item_list:
            intro_item_result = self.parse_intro_detail(html_text, intro_item)
            if intro_item_result:
                intro_var = intro_item.lower().replace(" ", "_")
                data[intro_var] = intro_item_result

        followed_by_details = self.parse_intro_detail(html_text, "Followed by")
        if followed_by_details:
            follower_number = re.findall(r"\d+", followed_by_details)
            data["followed_by"] = int("".join(follower_number))
        return dict(data=data)

    def parse_avatar(self, html_text):
        soup = self.bs(html_text)
        images = soup.findAll("image")
        avatar = ""
        if images:
            images = [x["xlink:href"] for x in soup.findAll("image")]
            try:
                image_sizes = [int(re.search(r"\d+x\d+", x).group().split("x")[0]) for x in images]
                avatar = images[image_sizes.index(max(image_sizes))]
            except AttributeError:
                for img in images:
                    if not re.search(r"\d+x\d+", img):
                        avatar = img
                        break
        return avatar

    # def parse_photos(self, html_text):
    #     soup = self.bs(html_text, "html.parser")
    #     # total_a_tags = soup.findAll("a", href=re.compile(".*photo/?fbid=.*"))
    #     total_a_tags = soup.find_all('a', {'href':re.compile('.*(photo/?fbid=).*')})
    #     print("total_a_tags: ", total_a_tags)
    #     for a_tag in total_a_tags:
    #         print(a_tag)
    #         # str_a_tag = str(a_tag)
    #         # with open("html.txt", "w", encoding="utf-8") as f:
    #         #     f.write(f"{str_a_tag}")
    #         # n_soup = self.bs(str_a_tag)
    #         images = a_tag.findAll("img")
    #         return [img["src"] for img in images if "scontent" in img["src"]]
    #     return []
