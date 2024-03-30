from requests import session
from requests.cookies import cookiejar_from_dict

session = session()


class BaseRequestHandler(object):

    def make_request(self, url, cookies=None):
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'connection': 'keep-alive',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36 '
        }
        response_data = session.get(url=url, cookies=cookiejar_from_dict(cookies), headers=header)
        return response_data

    def remove_cookies_un_use_prop(self, cookie):
        if "expirationDate" in cookie:
            del cookie["expirationDate"]
        if "sameSite" in cookie:
            del cookie["sameSite"]

    @staticmethod
    def make_post_request(url, payload):
        response_data = session.post(url=url, json=payload)
        return response_data
