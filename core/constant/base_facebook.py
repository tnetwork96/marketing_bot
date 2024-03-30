class Request:
    POST_URL = "https://graph.facebook.com/{}/feed?limit={}&access_token={}"
    LIMIT = 5
    ACCESS_TOKEN = "EAAGNO4a7r2wBAA6TtgZAilA0o6gilLaqFq79FNQgAa2MWwpoX0voA9ZA97guczbOQZAHpeG1enF" \
                   "gYC6mccGGmUfTm7Slx6FWJlZCIXM9YY6dKR6To10bsXVNG3ZAANQAdUhuA7PN1DYFzZCZA" \
                   "3cpCJbyFGWlVOuy91Ho5juU7qTZBgZDZD"
    GOOGLE_API_URL = "http://google_api_service:8000/google_sheet/field_value"
    # GOOGLE_API_URL = "http://192.168.1.4:8000/google_sheet/field_value"
    API_SERVICE = "api_service:8000"


class RelevantContent:
    CONTENT = [u"Mình tính ra(.*)chơi", u"Mình xin", u"Cho mình biết (.*) với", u"ăn quán nào"]


class CommentConstant:
    COMMENT = [u"Mời bạn thử hải sản tại quán"]
    LINK = "https://www.facebook.com/vongxoayseafood/"
