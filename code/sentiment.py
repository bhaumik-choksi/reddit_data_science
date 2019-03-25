from RedditHelper import RedditHelper

r = RedditHelper(cid='GKG50iWjxkkcew',
                 sec="6OKCI0V-OzGp5kx-fs7HN2QA_vM",
                 pwd='10488724593163d6045e1f53b56543f7',
                 ua='USERAGENT',
                 username='throwaway2244561')
print("getting data")
data = r.get_posts_and_comments(subreddit='politics')
print('proc')
sentiments = r.sentiment_analyze(data)
print(sentiments)

# sent analyze titles
# create freq table with sent values
