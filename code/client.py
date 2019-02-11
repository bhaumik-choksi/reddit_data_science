import praw
import numpy as np
from matplotlib import pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams
import sqlite3
import sys
import codecs
import re
import string
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
# import nltk
# nltk.download('stopwords')


############ Creates objects for emoji tokenizing ###########
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def tokenize_comments(comments):
    tokenized_comments = []
    for comment in comments:
        tokenized_comment = preprocess(comment)
        tokenized_comments.append(tokenized_comment)
    return tokenized_comments

def count_tokens(tokenized_comments):
    #gets list of punctuation
    punctuation = list(string.punctuation)
    #gets list of stopwords, appends punctuation
    stop = stopwords.words('english') + punctuation + ['’' , 'nbsp']
    #counts number of tokens in all comments
    count_all = Counter()
    for comment in tokenized_comments:
        tokens_all = []
        for token in comment:
            if token not in stop:
                tokens_all.append(token)
        count_all.update(tokens_all)
    return count_all

def get_bigram(tokens):
    #gets list of punctuation
    punctuation = list(string.punctuation)
    #gets list of stopwords, appends punctuation
    stop = stopwords.words('english') + punctuation + ['’' , 'nbsp']
    terms_stop = [term for term in tokens if term not in stop]
    terms_bigram = bigrams(terms_stop)
    return terms_bigram

# Auth
print ("authing...")
reddit = praw.Reddit(client_id='GKG50iWjxkkcew',
                     client_secret="6OKCI0V-OzGp5kx-fs7HN2QA_vM",
                     password='10488724593163d6045e1f53b56543f7',
                     user_agent='USERAGENT',
                     username='throwaway2244561')

# Selecting the subreddit
print ("Extracting top reddit posts...")
subreddit = "politics"
subreddit = reddit.subreddit(subreddit)
top_posts = subreddit.top(limit=10)

# Extract comments to list
print ("Extracting Comments...")
all_comments = []
for top_post in top_posts:
    title = top_post.title
    # print (title)
    comments = top_post.comments.list()
    for comment in comments[:100]:
        try:
            all_comments.append(comment.body.lower())
        except AttributeError as e:
            pass


# print (all_comments[1:11])
# preprocessing
print ("begining tokenizing...")
tokenized_comments = tokenize_comments(all_comments)
print (tokenized_comments[1])
token_count = count_tokens(tokenized_comments)
top_words = token_count.most_common(10)
print(top_words)

# bigrams = get_bigram(tokenized_comments)
# print (bigrams)




    # pos_sent = []
    # neg_sent = []
    # comp_sent = []

    # sid = SentimentIntensityAnalyzer()
    # for comment in comments:
    #     score = sid.polarity_scores(comment)
    #     # print(comment, score['compound'])
    #     pos_sent.append(score['pos'])
    #     neg_sent.append(score['neg'])
    #     comp_sent.append(score['compound'])

    # pos_sent = np.asarray(pos_sent)
    # neg_sent = np.asarray(neg_sent)

    # # Plotting
    # plt.scatter(pos_sent, neg_sent, cmap='seismic', c=comp_sent)
    # plt.show()
