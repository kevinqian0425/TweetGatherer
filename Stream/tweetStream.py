import json
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import data
import dataLoader

# ------------Keys for API---------- #
consumerKey = "eOOgZZpX8hmaPxIn0VoRbECil"
consumerSecret = "7rLhBiVALul0IYKcqbx0DRBajzPtYofO5Iw2Szv25rWhqmXFkW"
accessToken = "818157828921667584-6cTUK2RvwKdjpRevQ7msUE22sLcUUJi"
accessSecret = "SZBZKw10OAINbqQaCp5ZzUgQDXRPNkI2UhHDACmwafdIO"

# ------------ User Input ---------- #
fileName = "data"  # output will be in format data####.txt
keywords = "Civic, 2017"


# Creating Listener class that will gather data from API
class Listener(StreamListener):
    # Authentication worked and getting data

    def on_data(self, str_data):
        try:
            # data from on_data initially comes in as string. Converts to json
            data_json = json.loads(str_data)

            # Checking if keys exist in data
            if 'id' in data_json and 'text' in data_json and 'user' in data_json:
                try:
                    # if data.fileTrackerData['tweetNum'] % 1000 == 0:
                    #     data.fileTrackerData['tweetNum'] += 1
                    #     time.sleep(100)
                    fileNum = int(data.fileTrackerData['tweetNum'] / 10000)
                    if data.fileTrackerData['fileNum'] < fileNum:
                        data.fileTrackerData['fileNum'] += 1
                        dataLoader.update_file_tracker_data(
                            data.fileTrackerData['tweetNum'],
                            data.fileTrackerData['fileNum'])
                    print data.fileTrackerData
                    fileString = fileName + str(data.fileTrackerData['fileNum']) + '.txt'
                    saveFile = open(fileString, 'a')
                    saveFile.write(str_data)
                    saveFile.close()
                    data.fileTrackerData['tweetNum'] += 1
                    dataLoader.update_file_tracker_data(
                        data.fileTrackerData['tweetNum'],
                        data.fileTrackerData['fileNum'])
                    return True

                except BaseException, e:
                    print 'failed OnData: ', str(e)
                    time.sleep(5)
            return True

        # Could happen with bad internet... etc other errors
        except BaseException, e:
            print 'failed on_data,', str(e)
            time.sleep(5)

    # Happens when an error occurs - probably through a wrong key
    def on_error(self, status):
        print status
        if status == 420:  # 420 means maxed out on number of requests in a window of time
            # returning False in on_data disconnects the stream
            return False
        time.sleep(30)


# Setting Authentication Keys for API
auth = OAuthHandler(consumerKey, consumerSecret)
api = tweepy.API(auth)
auth.set_access_token(accessToken, accessSecret)
twitterStream = Stream(auth, Listener())

# Gathering tweets with keyword Trump
twitterStream.filter(track=[keywords])
