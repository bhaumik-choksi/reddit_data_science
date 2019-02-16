import praw
import heapq
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
from stop_words import get_stop_words
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize, WhitespaceTokenizer
from nltk.corpus import stopwords
from nltk import bigrams
import sys
import codecs
import re
import string
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



def preprocess(s, lowercase=False):
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
	tokens = tokens_re.findall(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens


def tokenize_sent(comments):
	sent_tokens = []
	for comment in comments:
		sents = sent_tokenize(comment)
		for s in sents:
			sent_tokens.append(s)
	return sent_tokens



def tokenize_words(comments):
	word_tokens = []
	for comment in comments:
		words = preprocess(comment)
		for w in words:
			word_tokens.append(w)
	return word_tokens


def filter_sent(sentence_list):
	stop_words = list(get_stop_words('en'))         #About 900 stopwords
	nltk_words = list(stopwords.words('english') + list(string.punctuation)+[ '’' ,'nbsp'])  #About 150 stopwords
	stop_words.extend(nltk_words)
	filtered_sentences = []
	for sent in sentence_list:
		sent = sent.lower()
		word_tokens = preprocess(sent)
		sentence = []
		for w in word_tokens:
			if w not in stop_words:
				sentence.append(w)
		filtered_sentences.append(sentence)
	return filtered_sentences



def filter_words(word_tokens):
	stop_words = list(get_stop_words('en'))         #About 900 stopwords
	nltk_words = list(stopwords.words('english') + list(string.punctuation)+[ '’', '“','”' ,'nbsp'])  #About 150 stopwords
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
list_of_frequencies.sort(key=(lambda x: x[1]), reverse=True)
print(list_of_frequencies[:10])




























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
