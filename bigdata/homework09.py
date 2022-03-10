


twitter_consumer_key='hZNwt5lHwgRPxz6xycUQ4hMGA'
twitter_consumer_secret='u7ZjOzNckOreyryCZgJFwSphfii73R8BP6h7oCJO2II0gkbTgM'
twitter_access_token='1382365106701357058-xtaya8aKnTb4VpQuRiRnMhnDNmhQSU'
twitter_access_secret='GnfKoeoADDhbURJI5c1kORxDsFRYdY9y4lfMq0QZ60c6I'

import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns
from matplotlib import font_manager,rc
from wordcloud import WordCloud
import platform
from konlpy.tag import Okt
from collections import Counter

auth =tweepy.OAuthHandler(twitter_consumer_key,twitter_consumer_secret)
auth.set_access_token(twitter_access_token,twitter_access_secret)
api=tweepy.API(auth)


tweetCriteria = got.manager.TweetCriteria().setUsername("realDonaldTrump")

"""
print(statuses)

for status in statuses:
    print(status.text)

output_file_name = "twitter_get_timeline_result.txt"
with open(output_file_name, "w", encoding="utf-8") as output_file:
    for status in statuses:
        print(status, file=output_file)

from collections import Counter

query = "#nthroom"
statuses = twitter_api.GetSearch(term=query, count=100)
result = []
for status in statuses:
    for tag in status.hashtags:
        result.append(tag.text)

Counter(result).most_common(20)

"""