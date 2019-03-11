import praw
import string
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#preprocessing
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from stop_words import get_stop_words
#word cloud libs
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt
#extractive text summarizing lib
from gensim.summarization import summarize
#utf stuff
import sys
import codecs
if sys.stdout.encoding != 'UTF-8':
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# import nltk
# nltk.download()


def get_comments(subreddit):
	reddit = praw.Reddit(client_id='GKG50iWjxkkcew',
						 client_secret="6OKCI0V-OzGp5kx-fs7HN2QA_vM",
						 password='10488724593163d6045e1f53b56543f7',
						 user_agent='USERAGENT',
						 username='throwaway2244561')

	# Selecting the subreddit
	subreddit = reddit.subreddit(subreddit)
	top_posts = subreddit.top(limit=2)
	# Extract comments to list
	all_comments = []
	for top_post in top_posts:
		title = top_post.title
		# print (title)
		comments = top_post.comments.list()
		for comment in comments[1:11]:
			try:
				all_comments.append(comment.body.lower())
			except AttributeError as e:
				pass
	return all_comments






def tokenize_sent(comments):
	sent_tokens = []
	for comment in comments:
		sents = sent_tokenize(comment)
		for s in sents:
			sent_tokens.append(s)
	return sent_tokens



def tokenize_words(comments):
	tokenizer = RegexpTokenizer(r'\w+')
	comment_tokens = []
	for comment in comments:
		tokens = tokenizer.tokenize(comment.lower())
		comment_tokens.append(tokens)
	word_tokens = []
	for comment in comment_tokens:
	    for word in comment:
	        word_tokens.append(word)
	return word_tokens


def filter_sent(sentence_list):
	tokenizer = RegexpTokenizer(r'\w+')
	stop_words = list(get_stop_words('en'))         #About 900 stopwords
	nltk_words = list(stopwords.words('english') + list(string.punctuation)+[ '’', '“','”' ,'nbsp','https','www','com'])  #About 150 stopwords
	stop_words.extend(nltk_words)
	filtered_sentences = []
	for sent in sentence_list:
		word_tokens = tokenizer.tokenize(sent.lower())
		sentence = []
		for w in word_tokens:
			if w not in stop_words:
				sentence.append(w)
		filtered_sentences.append(sentence)
	return filtered_sentences



def filter_words(word_tokens):
	stop_words = list(get_stop_words('en'))         #About 900 stopwords
	nltk_words = list(stopwords.words('english') + list(string.punctuation)+[ '’', '“','”' ,'nbsp','https','www','com'])  #About 150 stopwords
	stop_words.extend(nltk_words)
	output = []
	for w in word_tokens:
		w = w.lower()
		if w not in stop_words:
			output.append(w)
	return output


def sent_stemmer(sents):
	ps = PorterStemmer()
	stem_sent = []
	for sent in sents:
		temp = []
		for word in sent:
			stem_word = ps.stem(word)
			temp.append(stem_word)
		stem_sent.append(temp)
	stem_sent = list(filter(None, stem_sent))
	return stem_sent


def word_stemmer(words):
	ps = PorterStemmer()
	stem_words = []
	for word in words:
		stem_word = ps.stem(word)
		stem_words.append(stem_word)
	return stem_words


def count_tokens(words):
	word_frequencies = {}
	for word in words:
		if word not in word_frequencies:
			word_frequencies[word] = 1
		else:
			word_frequencies[word] += 1
	return word_frequencies


###################   Pre-Processing   #############################
def word_preprocess(comments):
	word_list = tokenize_words(comments)
	clean_words = filter_words(word_list)
	stem_words = word_stemmer(clean_words)
	return stem_words


def sent_preprocess(comments):
	sent_list = tokenize_sent(comments)
	clean_sent = filter_sent(sent_list)
	stem_sent = sent_stemmer(clean_sent)
	return stem_sent




# if __name__ == "__main__":
subreddit = "politics"
comments = get_comments(subreddit)
words = word_preprocess(comments)
sents = sent_preprocess(comments)
list_of_frequencies = list([k,v] for k,v in count_tokens(words).items())
list_of_frequencies = list_of_frequencies.sort(key=(lambda x: x[1]), reverse=True)


# summarize(comments, split=True)



































# dictionary = corpora.Dictionary(sents)
# print(dictionary)
# print("-------")
# print(dictionary.token2id)
# print("-------")
# bow_corpus = [dictionary.doc2bow(text) for text in sents]




# # train the model
# tfidf = models.TfidfModel(bow_corpus)
# # transform the "system minors" string
# tfidf[dictionary.doc2bow("system minors".lower().split())]






















































# print(list_of_frequencies[:10])

######
print ('starting')
with open('reddit_words.txt','wb') as w:
	for word in words:
		w.write(str(word).encode('utf-8')+b'\n')
print ('Done')

# print ('starting')
# with open('reddit_sent.txt','wb') as w:
# 	for sent in sents:
# 		w.write(str(sent).encode('utf8')+b'\n')
# print ('Done')

reddit_words = []
with open('reddit_words.txt', 'r') as r:
	for line in r:
		reddit_words.append(line.strip('\n'))
print(reddit_words)
text = ' '.join(map(str,reddit_words) )
wordcloud = WordCloud(max_font_size=50, background_color="black", max_words=40, colormap="nipy_spectral", regexp=r"\w[\w']+").generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



# reddit_words = []
# with open('reddit_words.txt', 'r') as r:
# 	for line in r:
# 		reddit_words.append(line.strip('\n'))
# print(reddit_words)




























#####################   Prototype code    ############################

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
