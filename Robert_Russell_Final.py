#Robert Russell
#Final Project CSC110
#Summer Quarter 2017 
#South Seattle Community College
#Emilia Gan

import random  #The random libray is used to select random tweets
import sys #The sys library helps exit the program gracefully
import datetime #The datetime library helps check user entered dates and format other dates in a uniform way
from contextlib import redirect_stdout #Making file output easier - hopefully 

trump_tweets = "TrumpTweetsTDL.txt"  #Loads a tab delimited file of Donald Trump tweets

#Create dictionaries for each column in the file

tweet_text = {}
tweet_time = {}
tweet_date = {}
tweet_comp = {}
tweet_fav = {}
tweet_rt = {}
tweet_neu = {}
tweet_pos = {}
tweet_neg = {}

#Keep count of how many tweets we're adding and how many are retweets - start at one to make things more sensible for humans
tweetid = 1
rt_by_trump = 1

for line in open(trump_tweets, 'r').readlines():  #Open the file and read line by line splitting columns on tabs.
    
    time, fav, rt, text, compound, neg, neu, pos = line.strip().split("\t")
    
    fav = int(fav)
    rt = int(rt)
    compound = float(compound)
    neg = float(neg)
    neu = float (neu)
    pos = float (pos)
    
        
    if fav != 0: #This logic prevents retweets from being included
        
        #Match each property of a tweet with an ID to make cross referencing easier.
        
        #This part can definitely be improved by using database calls instead of dictionaries. 
        #A nested dictionary may have been easier but I would want to time indexing performance before making the change
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

        
def basic_tweet_data(inp_id): #The most basic display of data about a tweet
    
    print('\nAt %s on %s the president tweeted:\n\n%s\n\nIt got %d favorites and was retweeted %d times\n-------' % (tweet_time[inp_id], tweet_date[inp_id], tweet_text[inp_id], tweet_fav[inp_id], tweet_rt[inp_id]))


def tweet_by_id(): #Allow user to call a tweet by its ID - useful later
    
    inp_id = int(input('Select a number between 1 and %d to view information about that tweet: ' % (tweetid -1)))
    
    if (inp_id >= 1 and inp_id <= (tweetid -1)):
        basic_tweet_data(inp_id)
        main_menu()
    
    else:
        print('Bad input - returning to main menu')
        main_menu()


def word_search(inp_word): #The function that handles searching tweets for a word

    tweets_contain = [] #This list holds the IDs of tweets that contain the word 
    for tweet in tweet_text:
        tweet_words = tweet_text[tweet]
        #Not case sensitive here. Also this method means that searching for 'is' would return a tweet with the text: This be a tweet. (due to 'is' being in 'This')
        #Due to the nature of "tweetspeak" this is probably the desired behavior. A more advanced option would involve regex.
        if inp_word.lower() in tweet_words.lower(): 
            tweets_contain.append(tweet)
            
    if len(tweets_contain) > 0: #Check if there were any results
        
        #Display a menu to handle the next action
        
        menu = input('The word %s appears at least once in %d of Trump\'s tweets. Would you like to see a list of the tweet (I)Ds, (a)ll of the contents of these tweets, (s)tatistics about this search, a (r)andom tweet containing %s, or the (m)ain menu? ' % (inp_word, len(tweets_contain), inp_word))
        
        
    elif len(tweets_contain) == 0: #Handle no results
        print('%s was not found in any of Trump\'s tweets.' % inp_word.title())
        main_menu()
    
    else: #This should never happen!
        print('Something has gone terribly wrong. Sorry!')
        sys.exit('tweets_contain variable was not a number greater than zero - somehow') #In the event that it somehow does manage to happen stderr will at least give a clue as to why. Maybe.

    #The if statements below could be split off in a separate function since other functions contain similar menus
    #However the way it's currently written it would have to include passing more variables in and out of the function to deal with the text specifically mentioning the word searched.
    
    if menu.lower() == ('s' or 'stats' or 'stat'):
        word_stats(tweets_contain, inp_word, 0)
        main_menu()
    
    if menu.lower() == ('i' or 'ids' or 'id'):

        if len(tweets_contain) > 1:

            tweets_contain_str = ', '.join(str(x) for x in tweets_contain[:-1])
            tweets_contain_str = tweets_contain_str + ', and ' + str(tweets_contain[-1]) #Make the string gramatically correct. What happens if there is only one result?? TEST THIS!
            print('The word %s appears in the following tweets:\n%s' % (inp_word, tweets_contain_str))

        elif len(tweets_contain) == 1:
            tweets_contain_str = ''.join(str(x) for x in tweets_contain)
            print('The word %s appears in the following tweet:\n%s' % (inp_word, tweets_contain_str))
                    
        main_menu()
    
    if menu.lower() == ('a' or 'all' or 'al' or 'all tweets'):
        
        for tweet in tweets_contain:
            basic_tweet_data(tweet)
            
        main_menu()
    
    if menu.lower() == ('r' or 'random' or 'rand' or 'rando'):
        
        for item in random.sample(tweets_contain, 1):
            random_tweet = item #Get the item in an int instead of a list. Why did I do this? Was it possible to just cast to int? (or string?)
            
        menu_random_tweet(random_tweet)
       
    if menu.lower() == ('m' or 'main' or 'menu' or 'main menu'):
        
        main_menu()
        
    else: #Bad input ends the program - consider changing to match behavior of other menus that allow second chances for bad input
        print('Goodbye')
        sys.exit(0)

def menu_random_tweet(inp_id): #What gets called when the main menu selection is random tweet
    
    basic_tweet_data(inp_id)
    main_menu()    
        

def menu_word_search(): #What gets called when the main menu selection is search for a word. Handles input and passes it to the detailed word search function
    inp_word = input('What word would you like to search for? (note this is not case sensitive) ')
    word_search(inp_word)
    
def main_menu(): #Added later to allow for a pause before returning to main menu.
    input('\nPress any key to return to the main menu')
    main_menu_1()

def main_menu_1(): #Changed from main_menu to add pause across all main_menu calls with the least amount of recoding
    
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
    

def date_search(inp_date): #This gets called when user wants to search by date
    tweets_contain = []
    for tweet in tweet_text:
        tweet_date_str = tweet_date[tweet]
        if inp_date == tweet_date_str:
            tweets_contain.append(tweet)
    
    #Everything below here in this function looks very familiar. As mentioned above it could be rewritten to be more modular with a little thoughtful variable passing and less specific text.        
                            
    if len(tweets_contain) > 0:
        menu = input('On %s Trump tweeted %d times. Would you like to see a list of the (i)ds, (a)ll the tweet text, or (r)andom tweet (or (m)ain menu)? ' % (inp_date, len(tweets_contain)))

    elif len(tweets_contain) == 0:
        print('\nNo tweets found for %s.  Maybe the format was wrong or perhaps out of the range of this program. Only tweets sent between %s and %s are indexed by this program ' % (inp_date, tweet_date[(tweetid-1)], tweet_date[1]))
        main_menu()
    
    else:
        print('Something has gone terribly wrong. Sorry!')
        sys.exit('tweets_contain variable was not a number greater than zero - somehow')
    
    if menu.lower() == ('i' or 'ids' or 'id'):
        
        if len(tweets_contain) > 1:
        
            tweets_contain_str = ', '.join(str(x) for x in tweets_contain[:-1])
            tweets_contain_str = tweets_contain_str + ', and ' + str(tweets_contain[-1])
            print('On %s the following tweets were sent:\n%s' % (inp_date, tweets_contain_str))
        
        elif len(tweets_contain) == 1:
            tweets_contain_str = ''.join(str(x) for x in tweets_contain)
            print('On %s the following tweet was sent:\n%s' % (inp_date, tweets_contain_str))
        
        main_menu()
    
    if menu.lower() == ('a' or 'all' or 'al' or 'all tweets'):
        
        for tweet in tweets_contain:
            basic_tweet_data(tweet)
            
        menu_save(tweets_contain, inp_date, 'date')
            
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

def menu_date_search(): #Gets called from main_menu_1 and handles date input before passing off to detailed date search
    
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

def word_stats(tweets_contain, inp_word, saving): #Called from the word search function to provide statistics about a single word.
    rt_total = 0
    fav_total = 0
    for tweet in tweets_contain:
        rt_total = int(rt_total) + tweet_rt[tweet]
        fav_total = int(fav_total) + tweet_fav[tweet]
    print('\nTweets where this word appeared at least once received a total of %d retweets, for an average of %d per tweet.' % (rt_total, (rt_total/len(tweets_contain))))
    print('Tweets where this word appeared at least once received a total of %d favorites, for an average of %d per tweet.\n' % (fav_total, (fav_total/len(tweets_contain))))
    
    #Compare the searched word's statistics to the overall averages.
    
    stats = overall_stats('rt') #pulls data from overall_stats function by passing variable that indicated it would like something back.
    
    if ((rt_total/len(tweets_contain))-(stats[1]/tweetid) > 0):
        print('\nTweets containing this word recieved %d more retweets than the average Trump tweet' % ((rt_total/len(tweets_contain))-(int(stats[1])/tweetid)))
        
    elif ((rt_total/len(tweets_contain))-(stats[1]/tweetid) < 0):
        print('\nTweets containing this word recieved %d fewer retweets than the average Trump tweet' % (((rt_total/len(tweets_contain))-(int(stats[1])/tweetid))/-1))
        
    if ((fav_total/len(tweets_contain))-(stats[0]/tweetid) > 0):
        print('Tweets containing this word recieved %d more favorites than the average Trump tweet' % ((fav_total/len(tweets_contain))-(int(stats[0])/tweetid)))
        
    elif ((fav_total/len(tweets_contain))-(stats[0]/tweetid) < 0):
        print('Tweets containing this word recieved %d fewer favorites than the average Trump tweet' % (((fav_total/len(tweets_contain))-(int(stats[0])/tweetid))/-1))
    
    if saving == True:
        return
        
    menu_save(tweets_contain, inp_word, 'word_stats')
    
    main_menu()
        
def overall_stats(req_stat): #Used for a main menu function as well as passing these stats to other functions.
    rt_total = 0
    fav_total = 0
    for tweet in tweet_rt:
        rt_total = int(rt_total) + tweet_rt[tweet]
    
    for tweet in tweet_fav:
        fav_total = int(fav_total) + tweet_fav[tweet]        
    
    if req_stat == 'rt': #Trigger to print this stat and return the values.
        print('Out of Trump\'s %d original tweets. The total favorites were %d and the total retweets by others were %d. This averages to %d favorites and %d retweets per tweet.' % (tweetid, fav_total, rt_total, (fav_total/tweetid), (rt_total/tweetid)))
        return fav_total, rt_total
    print('Out of a total of %d tweets, %d were tweets by other people that were retweeted by Trump and not analyzed for this program.\n' % ((tweetid + rt_by_trump), rt_by_trump))
    print('Out of Trump\'s %d original tweets. The total favorites were %d and the total retweets by others were %d. This averages to %d favorites and %d retweets per tweet.' % (tweetid, fav_total, rt_total, (fav_total/tweetid), (rt_total/tweetid)))
        

def menu_save(tweets_contain, user_data, data_type): #Create a menu that can be called anywhere to offer saving the output to a file if the user finds it interesting.
    
    save_inp = str(input('Did you find this interesting? Would you like to save it to a file for later review? y/n '))
    
    try:
        
        if save_inp.lower() == ('y' or 'yes'):
            
           save_file(tweets_contain, user_data, data_type)         
            
        elif save_inp.lower() == ('n' or 'no'):
            return
            
        else:
            print('Bad input, try again')
            menu_save(tweets_contain, user_data, data_type)
    except ValueError:
        print('Bad input - returning to main menu\n')
        main_menu_1()
        
def save_file(tweets_contain, user_data, data_type):

    file_name = str(user_data) + '_' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.txt' #Define a file name that makes sense but should be handled by all operating systems smoothly
    
    print('Your file has been saved as %s in the same directory this program was executed from.' % file_name)
    
    if data_type == 'word_stats':
        with open(file_name, 'w') as f:
            with redirect_stdout(f):
                basic_info()
                print('\n\n')
                print('The following is the analysis of the word %s in Donald Trump\'s tweets:\n' % user_data)
                word_stats(tweets_contain, user_data, 1)
    
    elif data_type == 'date':
        with open(file_name, 'w') as f:
            with redirect_stdout(f):
                basic_info()
                print('\n\n')
                print('On the date %s, Donald Trump tweeted:\n' % user_data)
                for tweet in tweets_contain:
                    basic_tweet_data(tweet)
        

def basic_info():
    print('This program was written as a final project for CSC110 class in Summer of 2017.')
    print('It analyzes tweets made by President Donald Trump from %s until %s. It does not inlcude things retweeted from his account.' % (tweet_date[(tweetid-1)], tweet_date[1]))
    print('I can\'t imagine anyone would want to use this for anything, but if you do - it\'s licensed under GPLv3')

                                                                        
main_menu_1() #Run the program

