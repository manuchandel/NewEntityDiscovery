import tweepy
import time
import re
import MySQLdb

# connecting to database
db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="LabBasedProject",charset='utf8' )
cursor=db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Twitter_Names (
    ID VARCHAR(50),
    NAME VARCHAR(100),
    SCREEN_NAME VARCHAR(50)
    ) ENGINE=InnoDB
    """)

consumer_key='xxxx'
consumer_secret='xxxx'
access_token='xxxx'
access_token_secret='xxxx'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def read_unicode(text, charset='utf-8'):
    if isinstance(text, basestring):
        if not isinstance(text, unicode):
            text = unicode(obj, charset)
    return text

def write_unicode(text, charset='utf-8'):
    return text.encode(charset)


c= tweepy.Cursor(api.followers, screen_name="SrBachchan",count=199).items()
names_fetched=0
while True:
    try:
        user = c.next()
        twitter_id=write_unicode(user.id_str)
        twitter_name=write_unicode(user.name) 
        twitter_screen_name=write_unicode(user.screen_name)

        if re.match("^[A-Za-z ]*$",twitter_name):
            cursor.execute("INSERT INTO `Twitter_Names` (`ID`,`NAME`,`SCREEN_NAME`) VALUES (%s,%s,%s)",(twitter_id,twitter_name,twitter_screen_name))
            names_fetched+=1

    except tweepy.TweepError:
        if names_fetched >0:
            print names_fetched
            names_fetched=0
            db.commit()
        time.sleep(60*5)
        continue
    except StopIteration:
        break
	
