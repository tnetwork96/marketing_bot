class BrowserOptionConstant:
    """Request constant for AWS Lambda function"""
    HEADLESS = "--headless"
    NO_SANDBOX = "--no-sandbox"
    PERMISSIONS_DEFAULT_STYLESHEET = "permissions.default.stylesheet"
    PERMISSIONS_DEFAULT_IMAGE = "permissions.default.image"
    JAVASCRIPT_ENABLED = "javascript.enabled"
    SINGLE_PROCESS = "--single-process"
    DISABLE_DEV_SHM_USAGE = "--disable-dev-shm-usage"
    WINDOWS_SIZE = "--window-size={},{}"


class CookieConstant:
    NAME = "name"
    VALUE = "value"
    WD = "wd"
    EXPIRY = "expiry"
    SAME_SITE = "sameSite"
    LAST_TIME_REQUEST = "last_time_request"
    REQUEST_COUNT = "request_count"
    COOKIE = "cookie"
    STATUS = "status"
    ALIVE = "alive"
    NEED_CONFIRM = "need_confirm"
    BAN = "ban"


class JSConstant:
    WINDOW_SCROLL_TO = "window.scrollTo({}, {});"


class DriverPathConstant:
    CHROME_DRIVER = "geckodriver.exe"
    HEADLESS_CHROME = "/usr/local/bin/headless-chromium"


class SNSMessageConstant:
    COOKIE_EXPIRED = "Cookie expired"
    NO_ALIVE_COOKIE_FOUND = "Alive cookie not found"


class FacebookXPath:
    USERNAME_FORM = "//input[@name='email']"
    PASSWORD_FORM = "//input[@name='pass']"
    LOGIN_BUTTON = "//button[@name='login']"
    SEARCH_FORM = '//input[@placeholder="Search Facebook"]'
    ENTER_CODE = '//input[@placeholder="Enter code"]'
    CONTACT_PATTERN = "//span[contains(.,'Contacts')]"
    API_REQUEST_BOX = '//input[@role="combobox"]'
    API_DEBUG_INFORMATION = "//div[contains(.,'Copy Debug Information')]"
    SEARCH_MOBILE_FORM = "//span[contains(.,'Search')]"
    WHAT_ON_YOUR_MIND = '//div[@aria-label="Make a Post on Facebook"]'
    CHOOSE_A_GIF_LABEL = '//div[@aria-label="Choose a gif"]'
    FIND_FRIEND_BUTTON = "//span[contains(.,'Find friends')]"
    FACEBOOK_LOGO = "//a[@aria-label='Facebook']"
    LIKE_BUTTON = '//div[@aria-label="Like"]'
    ALL_REACTION = "//div[contains(.,'All reactions:')]"
    SEARCH_TEXT = "//input[@placeholder='Search']"
    ABOUT_TAB = "//span[contains(.,'About')]"
    ACTIVITY_LABEL = "//span[contains(.,'New activity')]"
    POST_PATTERN = "//span[contains(.,'...')]"
    WRITE_COMMENT_PATTERN = "//div[@aria-label='Write a comment']"
    WRITE_ANSWER_PATTERN = "//div[@aria-label='Write an answer…']"
    WRITE_SOMETHING = "//span[contains(.,'Write something...')]"
    WRITE_PUBLIC_COMMENT_PATTERN = "//div[@aria-label='Write a public comment…']"
    DISCUSSION_PATTERN = "//span[contains(.,'Discussion')]"
    JOINED_GROUP_PATTERN = "//div[@aria-label='Joined']"
    MORE_GROUP_PATTERN = "//div[@aria-label='More']"
    FEED_PATTERN = "//div[@role='feed']"
    GROUP_FEED_PATTERN = "//div[@data-pagelet='GroupFeed']"
    ARTICLE_PATTERN = "//div[@role='article']"
    TEXT_AUTO_PATTERN = "//span[@dir='auto']"
    MESSAGE_POST_PATTERN = "//div[@data-ad-comet-preview='message']"
    MESSAGE_TEXT_PATTERN = '//div[@style="text-align: start;"]'
    NEW_ACTIVITY_PATTERN = "//span[contains(.,'New activity')]"
    RECENT_POSTS_PATTERN = "//span[contains(.,'Recent posts')]"
    LABEL_PATTERN = "//a[@aria-label='label']"
    LINK_PATTERN = "//a[@role='link']"
    FIND_MEMBERS_PATTERN = "//input[@placeholder='Find a member']"
    SEARCH_MESSENGER_PATTERN = "//input[@placeholder='Search Messenger']"
    MESSAGE_BOX = "//div[contains(.,'Aa')]"
    SEARCH_MEMBERS_PATTERN = "//input[@placeholder='Search']"
    SHARE_BUTTON = "//div[@aria-label='Send this to friends or post it on your timeline.']"
    CONFIRM_BUTTON = "//div[@aria-label='Confirm']"
    CONFIRM_SMS_BUTTON = "//div[contains(.,'Confirm')]"
    REMOVE_LIKE_BUTTON = "//div[@aria-label='Remove Like']"
    LIST_ITEM_PATTERN = "//div[@role='listitem']"
    INTRO_PATTERN = "//span[contains(.,'Intro')]"
    FRIEND_PATTERN = "//span[contains(.,'Friends')]"
    FRIEND_REQUEST_PATTERN = "//span[contains(.,'Friend Requests')]"
    ADD_FRIEND_BUTTON = "//div[@aria-label='Add Friend']"
    ADD_FRIEND_WARNING = "//span[contains(.,'Add Friend')]"
    BUSSINESS_STORES_PATTERN = "//span[contains(.,'Stores')]"
    TOKEN_GEN_PATTERN = "//div[contains(.,'Generate Access Token')]"


class GoogleXpath:
    SEARCH_IN_GMAIL_PATTERN = "//input[@aria-label='Search in mail']"
    LOGIN_LABEL = "//span[contains(.,u'Đăng nhập')]"
    SEARCH_IN_YOUTUBE_PATTERN = "//input[@id='Search']"
    SEARCH_IN_GOOGLE_PATTERN = "//input[@value='Google Search']"


class FacebookUrl:
    FACEBOOK_URL = "https://www.facebook.com/{}"
    M_FACEBOOK_URL = "https://m.facebook.com/{}"
    FACEBOOK_GROUP_URL = "https://www.facebook.com/groups/{}?sorting_setting=CHRONOLOGICAL"
    FACEBOOK_MEMBERS_NEAR_U_URL = "{}/members/near_you"


class GoogleUrl:
    GOOGLE_URL = "https://google.com/"
    GMAIL_URL = "https://gmail.com/{}"
    YOUTUBE_URL = "https://youtube.com/"


class VietSchool:
    XEM_PATTERN = "//a[contains(.,'HỎI ĐÁP')]"


class LanIT:
    USERNAME_LOGIN = "//input[@id='username']"
    PW_LOGIN = "//input[@id='_password']"
    LOGIN_BUTTON = "//input[@id='login']"
    VPS_CONTROL_PANEL = "//li[@id='lmlistvs']"
    VPS_PRICE_PANEL = "//li[@id='lmcreate']"


class ZomRo:
    ORDER_BUTTON = "//button[contains(., 'Order')]"
    SERVICE_LABEL = "//h3[@class='ServicesPage_page_title__rCCLC']"

class OpNet:
    shop_now_label = "//a[contains(text(), 'Shop now')]"