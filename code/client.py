import praw
import numpy as np
from matplotlib import pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Auth
reddit = praw.Reddit(client_id='GKG50iWjxkkcew',
                     client_secret="6OKCI0V-OzGp5kx-fs7HN2QA_vM",
                     password='10488724593163d6045e1f53b56543f7',
                     user_agent='USERAGENT',
                     username='throwaway2244561')

print(reddit.user.me())

# Selecting the subreddit
subreddit = reddit.subreddit('politics')
tops = subreddit.top(limit=1)

# Browsing posts
for top_post in tops:
    title = top_post.title
    print("Title", title)
    comments = []

    # Browsing comments
    all_comments = top_post.comments.list()
    for comment in all_comments[:50]:
        comments.append(comment.body)

    pos_sent = []
    neg_sent = []
    comp_sent = []

    sid = SentimentIntensityAnalyzer()
    for comment in comments:
        score = sid.polarity_scores(comment)
        # print(comment, score['compound'])
        pos_sent.append(score['pos'])
        neg_sent.append(score['neg'])
        comp_sent.append(score['compound'])

    pos_sent = np.asarray(pos_sent)
    neg_sent = np.asarray(neg_sent)

    # Plotting
    plt.scatter(pos_sent, neg_sent, cmap='seismic', c=comp_sent)
    plt.show()
