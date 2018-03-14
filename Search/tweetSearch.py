import xlwt

import tweepy
from tweepy import OAuthHandler

# ------------------ What you want to Find -------------------- #
# How to use Keywords:
# To input multiple phrases, Separate your strings with a commas
# ex: "Car" will find anything with
# ex: "Red Car" Will find anything with red and car in that exact format (i.e. This is a red car)
# ex: "Red, Car" Will find anything with Red and Car in the same sentence (i.e. I have a Car. I have a Red Apple)
# NOTE* Dates acn only go back 2 week in time!

#####################################################################################################
# Note that If you have too many items, i.e. 10,000 and there are 10,000 tweets, you will receive a #
# status code = 429 error - or too many requests.                                                   #
# IF YOU GET THIS ERROR. WAIT AT LEAST AN HOUR BEFORE TRYING AGAIN. REDUCE numTweets variable too       #
#####################################################################################################

# ---------------- Input ------------------------ #

keywords = "Jeff, Sessions"
excelSheetName = "jeffsessions.xls"
beginSearchDate = "2017-04-08"
endSearchDate = "2017-04-22"
numTweets = 5000

# ---------------- Access Keys ------------------#
consumerKey = "eOOgZZpX8hmaPxIn0VoRbECil"
consumerSecret = "7rLhBiVALul0IYKcqbx0DRBajzPtYofO5Iw2Szv25rWhqmXFkW"
accessToken = "818157828921667584-6cTUK2RvwKdjpRevQ7msUE22sLcUUJi"
accessSecret = "SZBZKw10OAINbqQaCp5ZzUgQDXRPNkI2UhHDACmwafdIO"

auth = OAuthHandler(consumerKey, consumerSecret)
api = tweepy.API(auth)
auth.set_access_token(accessToken, accessSecret)


# ------------ Tweet Extraction Functions ---------- #
def get_text(string):
    string_buffer = string.split("text=")
    text = string_buffer[1].split(", ")
    return text[0]


def get_screen_name(string):
    string_buffer = string.split("screen_name=u'")
    text = string_buffer[1].split("',")
    return text[0]


def get_retweet_count(string):
    string_buffer = string.split("retweet_count=")
    text = string_buffer[1].split(",")
    return text[0]


def get_user_data(api, username):
    user_data = api.get_user(username)
    return user_data


# ----------- Using Excel Sheet ------------ $
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 0, "Keywords: " + keywords)
sheet1.write(0, 1, "Begin Date: " + beginSearchDate)
sheet1.write(0, 2, "End Date: " + endSearchDate)
sheet1.write(1, 0, "Tweet")
sheet1.write(1, 1, "Verified")
sheet1.write(1, 2, "Irrelevant")
sheet1.write(1, 3, "Username")
sheet1.write(1, 4, "userID")
sheet1.write(1, 5, "Tweet Length")
sheet1.write(1, 6, "Retweet Count")
sheet1.write(1, 7, "Friends Count")
sheet1.write(1, 8, "Followers Count")
sheet1.write(1, 9, "Status Count")
sheet1.write(1, 10, "Favorites Count")
sheet1.write(1, 11, "List Count")
sheet1.write(1, 12, "Created_At")
sheet1.write(1, 13, "Description")
sheet1.write(1, 14, "Location")
sheet1.write(1, 15, "verified")
sheet1.write(1, 16, "profile_use_background_image")
sheet1.write(1, 17, "default_profile_image")

# ------------ Iterating Through Tweets ------------ #
counter = 2

for tweet in tweepy.Cursor(api.search,
                           q=keywords,
                           since=beginSearchDate,
                           until=endSearchDate,
                           lang="en").items(numTweets):  # Maximum 2000 Tweets

    tweet_string = str(tweet)

    # Used to Skip "Reply Tweets"
    if tweet_string.find('RT') > 0:  # Returns index if found. Returns -1 if not found
        continue

    # Parsing through for Tweet Data
    tweet_data = {}
    tweet_data['text'] = get_text(tweet_string)
    tweet_data['screen_name'] = get_screen_name(tweet_string)
    tweet_data['retweet_count'] = get_retweet_count(tweet_string)

    # Get User Data
    user_data = get_user_data(api, tweet_data['screen_name'])
    tweet_data['friends_count'] = str(user_data.friends_count)
    tweet_data['favorite_count'] = str(user_data.favourites_count)
    tweet_data['status_count'] = str(user_data.statuses_count)
    tweet_data['list_count'] = str(user_data.listed_count)
    tweet_data['followers_count'] = str(user_data.followers_count)
    tweet_data['id_str'] = str(user_data.id)
    tweet_data['created_at'] = str(user_data.created_at)
    tweet_data['verified'] = str(user_data.verified)
    tweet_data['profile_use_background_image'] = str(user_data.profile_use_background_image)
    tweet_data['default_profile_image'] = str(user_data.default_profile_image)
    try:
        tweet_data['description'] = str(user_data.description)
    except Exception, e:
        tweet_data['description'] = " "
    try:
        tweet_data['location'] = str(user_data.location)
    except Exception, e:
        tweet_data['location'] = " "
    # Preventing Error in the case that user does not set their description of location

    # Writing Data to Excel Sheet
    sheet1.write(counter, 0, tweet_data['text'])
    sheet1.write(counter, 3, tweet_data['screen_name'])
    sheet1.write(counter, 4, tweet_data['id_str'])
    sheet1.write(counter, 5, len(tweet_data['text'].split()))
    sheet1.write(counter, 6, tweet_data['retweet_count'])
    sheet1.write(counter, 7, tweet_data['friends_count'])
    sheet1.write(counter, 8, tweet_data['followers_count'])
    sheet1.write(counter, 9, tweet_data['status_count'])
    sheet1.write(counter, 10, tweet_data['favorite_count'])
    sheet1.write(counter, 11, tweet_data['list_count'])
    sheet1.write(counter, 12, tweet_data['created_at'])
    sheet1.write(counter, 13, tweet_data['description'])
    sheet1.write(counter, 14, tweet_data['location'])
    sheet1.write(counter, 15, tweet_data['verified'])
    sheet1.write(counter, 16, tweet_data['profile_use_background_image'])
    sheet1.write(counter, 17, tweet_data['default_profile_image'])
    counter += 1
    book.save(excelSheetName)
