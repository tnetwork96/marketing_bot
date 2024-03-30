from sn.facebook.functions.crawl_profile.crawl_profile import ProfileCrawler

a = ProfileCrawler()
data = a.get_profile_data(username="100011289941300")
print("data: ", data)