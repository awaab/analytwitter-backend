import GetOldTweets3 as got
from datetime import date

# Searches for tweets until today
def get_tweets(search_term,top=True,tweet_num=150):
	today = date.today().strftime("%Y-%m-%d")
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_term)\
	.setUntil(today)\
	.setMaxTweets(tweet_num)\
	.setLang('en')\
	.setTopTweets(top)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	return tweets