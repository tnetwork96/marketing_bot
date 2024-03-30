import json

from requests import session
from core.constant.facebook_header import HEADER
import re

s = session()

class GetToken(object):
    def __init__(self, cookies):
        self.cookies = cookies
        self.add_cookies_to_session()

    def add_cookies_to_session(self):
        for ck in self.cookies:
            s.cookies.set(ck["name"], ck["value"])
    def get_token(self):
        data = s.get('https://business.facebook.com/business_locations', headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 '
                          'Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.86 Mobile Safari/537.36',
            'referer': 'https://www.facebook.com/',
            'host': 'business.facebook.com',
            'origin': 'https://business.facebook.com',
            'upgrade-insecure-requests': '1',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'accept': 'Mozilla/5.0 (X11; Linux armv7l; rv:102.0) Gecko/20100101 Firefox/102.0',
            'content-type': 'text/html; charset=utf-8'
        })
        find_token = re.search('(EAAG\w+)', data.text)
        if not find_token:
            results = ""
        else:
            results = find_token.group(1)
        return results

    def build_cookie_header(self, cookies):
        temp = list()
        for ele in cookies:
            temp.append(f'{ele.name}={ele.value}')
        return '; '.join(temp)

    def get_api_resp(self, token):
        """EAAGNO4a7r2wBAFcFXawINCZA0hvdXWwj8eclmkBay2hkDeN1RKoHV43vSjH3e7nRMzNsZATvLLMGNFwlvhhg6lvQ49MkO6Y655502bOXTNEBVRWpoagVZCaiZB9CHRkzu45G05lG2m2bVjH8jZBzE5IH2pzADiJfBhx6fMDlrMo9RAIknRaRk2rFrjbeicDEZD"""
        HEADER.graph_api_header["cookie"] = self.build_cookie_header(s.cookies)
        print("header: ", HEADER.graph_api_header)
        url = f'https://graph.facebook.com/v15.0/100070435330090/feed?access_token={token}&fields=id%2Cname&format=json&method=get&pretty=0&suppress_http_code=1&transport=cors'
        result = s.get(url).json()
        return result

