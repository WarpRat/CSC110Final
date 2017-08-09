import random
import sys
import datetime

trump_tweets = "TrumpTweetsTDL.txt"

tweet_text = {}
tweet_time = {}
tweet_date = {}
tweet_comp = {}
tweet_fav = {}
tweet_rt = {}
tweet_neu = {}
tweet_pos = {}
tweet_neg = {}
tweetid = 1
rt_by_trump = 1

for line in open(trump_tweets, 'r').readlines():
    
    time, fav, rt, text, compound, neg, neu, pos = line.strip().split("\t")
    
    fav = int(fav)
    rt = int(rt)
    compound = float(compound)
    neg = float(neg)
    neu = float (neu)
    pos = float (pos)
    
        
    if fav != 0:
        
        time = time.split()
        tweet_date[tweetid] = time[0]
        tweet_time[tweetid] = time[1]
        tweet_text[tweetid] = text
        tweet_comp[tweetid] = compound
        tweet_fav[tweetid] = fav
        tweet_rt[tweetid] = rt
        tweet_neu[tweetid] = neu
        tweet_pos[tweetid] = pos
        tweet_neg[tweetid] = neg
        tweetid += 1
        
    elif fav == 0:
        
        rt_by_trump += 1

        
def basic_tweet_data(inp_id):
    print('\nAt %s on %s the president tweeted:\n\n%s\n\nIt got %d favorites and was retweeted %d times\n-------' % (tweet_time[inp_id], tweet_date[inp_id], tweet_text[inp_id], tweet_fav[inp_id], tweet_rt[inp_id]))

def tweet_by_id():
    inp_id = int(input('Select a number between 1 and %d to view information about that tweet: ' % (tweetid -1)))
    
    if (inp_id >= 1 and inp_id <= (tweetid -1)):
        basic_tweet_data(inp_id)
        main_menu()
    
    else:
        print('Bad input - returning to main menu')
        main_menu()

def word_search(inp_word):
    tweets_contain = []
    for tweet in tweet_text:
        tweet_words = tweet_text[tweet]
        if inp_word.lower() in tweet_words.lower():
            tweets_contain.append(tweet)
            
    if len(tweets_contain) > 0:
        menu = input('The word %s appears at least once in %d of Trump\'s tweets. Would you like to see a list of the tweet (I)Ds, (a)ll of the contents of these tweets, (s)tatistics about this search, a (r)andom tweet containing %s, or the (m)ain menu? ' % (inp_word, len(tweets_contain), inp_word))
        
        
    elif len(tweets_contain) == 0:
        print('%s was not found in any of Trump\'s tweets.' % inp_word.title())
        main_menu()
    
    else:
        print('Something has gone terribly wrong. Sorry!')
        sys.exit('tweets_contain variable was not a number greater than zero - somehow')
    
    if menu.lower() == ('s' or 'stats' or 'stat'):
        word_stats(tweets_contain)
        main_menu()
    
    if menu.lower() == ('i' or 'ids' or 'id'):

        tweets_contain_str = ', '.join(str(x) for x in tweets_contain[:-1])
        tweets_contain_str = tweets_contain_str + ', and ' + str(tweets_contain[-1])
        print('The word %s appears in the following tweets:\n%s' % (inp_word, tweets_contain_str))
        
        main_menu()
    
    if menu.lower() == ('a' or 'all' or 'al' or 'all tweets'):
        
        for tweet in tweets_contain:
            basic_tweet_data(tweet)
            
        main_menu()
    
    if menu.lower() == ('r' or 'random' or 'rand' or 'rando'):
        
        for item in random.sample(tweets_contain, 1):
            random_tweet = item 
            
        menu_random_tweet(random_tweet)
       
    if menu.lower() == ('m' or 'main' or 'menu' or 'main menu'):
        
        main_menu()
        
    else:
        print('Goodbye')
        sys.exit(0)

def menu_random_tweet(inp_id):
    
    basic_tweet_data(inp_id)
    main_menu()    
        

def menu_word_search():
    inp_word = input('What word would you like to search for? (note this is not case sensitive) ')
    word_search(inp_word)
    
def main_menu():
    input('\nPress any key to return to the main menu')
    main_menu_1()

def main_menu_1():
    menu = input('\nMain Menu:\n(S)earch for a word or phrase\n(R)andom tweet\nTweet data by (I)D\n(O)verall Statistics\n(T)ime and Date Search\n(Q)uit\n?')
    
    if menu.lower() == ('s' or 'search' or 'find'):
        menu_word_search()
    
    if menu.lower() == ('r' or 'random' or 'rando'):
        rand_id = random.randrange(tweetid)
        menu_random_tweet(rand_id)
        
    if menu.lower() == ('i' or 'id'):
        tweet_by_id()
    
    if menu.lower() ==('t' or 'time' or 'd' or 'date'):
        menu_date_search()
    
    if menu.lower() == ('q' or 'quit' or 'x' or 'exit'):
        sys.exit(0)
        
    else:
        print('\n\n\n\nBad input - try again')
        main_menu()
    

def date_search(inp_date):
    tweets_contain = []
    for tweet in tweet_text:
        tweet_date_str = tweet_date[tweet]
        if inp_date == tweet_date_str:
            tweets_contain.append(tweet)
            
    if len(tweets_contain) > 0:
        menu = input('On %s Trump tweeted %d times. Would you like to see a list of the (i)ds, (a)ll the tweet text, or (r)andom tweet (or (m)ain menu)? ' % (inp_date, len(tweets_contain)))

    elif len(tweets_contain) == 0:
        print('\nNo tweets found for %s.  Maybe the format was wrong or perhaps out of the range of this program. Only tweets sent between %s and %s are indexed by this program ' % (inp_date, tweet_date[(tweetid-1)], tweet_date[0]))
        main_menu()
    
    else:
        print('Something has gone terribly wrong. Sorry!')
        sys.exit('tweets_contain variable was not a number greater than zero - somehow')
    
    if menu.lower() == ('i' or 'ids' or 'id'):
        tweets_contain_str = ', '.join(str(x) for x in tweets_contain[:-1])
        tweets_contain_str = tweets_contain_str + ', and ' + str(tweets_contain[-1])
        print('On %s the following tweets were sent:\n%s' % (inp_date, tweets_contain_str))
        
        main_menu()
    
    if menu.lower() == ('a' or 'all' or 'al' or 'all tweets'):
        
        for tweet in tweets_contain:
            basic_tweet_data(tweet)
            
        main_menu()
    
    if menu.lower() == ('r' or 'random' or 'rand' or 'rando'):
        
        for item in random.sample(tweets_contain, 1):
            random_tweet = item 
            
        menu_random_tweet(random_tweet)
       
    if menu.lower() == ('m' or 'main' or 'menu' or 'main menu'):
        
        main_menu()
        
    else:
        print('Goodbye')
        sys.exit(0)

def menu_date_search(): 
    
    inp_date = input('Please enter date in YYYY-MM-DD format: ')  #Get user input for the date they want to search
    
    try: 
        
        if inp_date[2] == ('-' or '/' or ' '):  #Examine the third character entered. If the year was written in short form, silently correct it
            inp_date = '20' + inp_date  
        
        if (int(inp_date[5:7]) > 12 and int(inp_date[8:10]) < 12): #See if it looks like the user entered the date and month backwards - silently flip if so.
            buffer =[]
            buffer.append(inp_date[5:7])
            buffer.append(inp_date[8:])
            inp_date = inp_date[:4] + ' ' + buffer[1] + ' ' + buffer[0]
    except ValueError:
        print('Wrong format')
        menu_date_search()
    except IndexError:
        print('Wrong format')
        menu_date_search()
        
    try:
        datetime.date(int(inp_date[0:4]), int(inp_date[5:7]), int(inp_date[8:10])).isoformat() #make sure that it's a real date format
    except ValueError:
        print('Wrong format')
        menu_date_search()
    
    clean_inp_date = datetime.date(int(inp_date[0:4]), int(inp_date[5:7]), int(inp_date[8:10])).isoformat() #Have python generate a date to ensure clean input
    date_search(clean_inp_date)

def word_stats(tweets_contain):
    rt_total = 0
    fav_total = 0
    for tweet in tweets_contain:
        rt_total = int(rt_total) + tweet_rt[tweet]
        fav_total = int(fav_total) + tweet_fav[tweet]
    print('\nTweets where this word appeared at least once received a total of %d retweets, for an average of %d per tweet.' % (rt_total, (rt_total/len(tweets_contain))))
    print('Tweets where this word appeared at least once received a total of %d favorites, for an average of %d per tweet.\n' % (fav_total, (fav_total/len(tweets_contain))))
    #compare to overall stats here   
    stats = overall_stats('rt')
    
    if ((rt_total/len(tweets_contain))-(stats[1]/tweetid) > 0):
        print('\nTweets containing this word recieved %d more retweets than the average Trump tweet' % ((rt_total/len(tweets_contain))-(int(stats[1])/tweetid)))
        
    elif ((rt_total/len(tweets_contain))-(stats[1]/tweetid) < 0):
        print('\nTweets containing this word recieved %d fewer retweets than the average Trump tweet' % (((rt_total/len(tweets_contain))-(int(stats[1])/tweetid))/-1))
        
    if ((fav_total/len(tweets_contain))-(stats[0]/tweetid) > 0):
        print('Tweets containing this word recieved %d more favorites than the average Trump tweet' % ((fav_total/len(tweets_contain))-(int(stats[0])/tweetid)))
        
    elif ((fav_total/len(tweets_contain))-(stats[0]/tweetid) < 0):
        print('Tweets containing this word recieved %d fewer favorites than the average Trump tweet' % (((fav_total/len(tweets_contain))-(int(stats[0])/tweetid))/-1))
    main_menu()
        
def overall_stats(req_stat):
    rt_total = 0
    fav_total = 0
    for tweet in tweet_rt:
        rt_total = int(rt_total) + tweet_rt[tweet]
    
    for tweet in tweet_fav:
        fav_total = int(fav_total) + tweet_fav[tweet]        
    
    if req_stat == 'rt':
        print('Out of Trump\'s %d original tweets. The total favorites were %d and the total retweets by others were %d. This averages to %d favorites and %d retweets per tweet.' % (tweetid, fav_total, rt_total, (fav_total/tweetid), (rt_total/tweetid)))
        return fav_total, rt_total
    print('Out of a total of %d tweets, %d were tweets by other people that were retweeted by Trump and not analyzed for this program.\n' % ((tweetid + rt_by_trump), rt_by_trump))
    print('Out of Trump\'s %d original tweets. The total favorites were %d and the total retweets by others were %d. This averages to %d favorites and %d retweets per tweet.' % (tweetid, fav_total, rt_total, (fav_total/tweetid), (rt_total/tweetid)))
        
            
main_menu_1()
