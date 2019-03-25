import praw
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class RedditHelper:
    def __init__(self, cid, sec, pwd, username, ua="USERAGENT"):
        self.reddit_instance = praw.Reddit(client_id=cid, client_secret=sec, password=pwd, user_agent=ua,
                                           username=username)

    def get_posts_and_comments(self, subreddit, n_posts=5, n_comments=5):
        
        subreddit_instance = self.reddit_instance.subreddit(subreddit)
        top_posts = subreddit_instance.top(limit=n_posts)
        data = []

        for post in top_posts:
            post_data = {'title': post.title}
            comments_list = []
            comments = post.comments.list()
            for comment in comments[1:n_comments + 1]:
                try:
                    comments_list.append(comment.body.lower())
                except:
                    pass

            post_data['comments'] = comments_list
            data.append(post_data)
        return data

    def sentiment_analyze(self, data):
        stop_words = list(get_stop_words('en'))  # About 900 stopwords
        nltk_words = list(
            stopwords.words('english') + list(string.punctuation) + ['’', '“', '”', 'nbsp', 'https', 'www',
                                                                     'com'])  # About 150 stopwords
        stop_words.extend(nltk_words)

        word_wise_sentiments = {}
        for item in data:
            title = item['title']
            comments = item['comments']
            compound_sent_score = 0
            sid = SentimentIntensityAnalyzer()
            for comment in comments:
                compound_sent_score += sid.polarity_scores(comment)['compound']
            compound_sent_score /= len(comments)

            noun_list = TextBlob(title).noun_phrases
            for noun_word in noun_list:
                if noun_word in word_wise_sentiments:
                    word_wise_sentiments[noun_word].append(compound_sent_score)
                else:
                    word_wise_sentiments[noun_word] = [compound_sent_score]

        for word, scores in word_wise_sentiments.items():
            word_wise_sentiments[word] = sum(scores)/len(scores)

        return word_wise_sentiments


