import pickle, h5py
from tensorflow.python.keras import backend as K
import tensorflow as tf
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.backend import set_session
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
import os.path
import numpy as np
import string
import re
from textblob import TextBlob

BASE = os.path.dirname(os.path.abspath(__file__))

global graph,model

tf_config = tf.ConfigProto()
sess = tf.Session(config=tf_config)
set_session(sess)

graph = tf.get_default_graph()
model = load_model(os.path.join(BASE, "ml_models/twit_sent_model.h5"))
with open(os.path.join(BASE, "ml_models/tokenizer.pickle"), 'rb') as handle:
    tokenizer = pickle.load(handle)

max_tokens =  model.layers[0].input_shape[1]

def predict(sent):
  #sent = ['this is cool']
  tokenized_sent = tokenizer.texts_to_sequences(sent)
  padded_tokenized_sent = pad_sequences(tokenized_sent, maxlen=max_tokens,
                              padding='pre', truncating='pre')
  return model.predict(padded_tokenized_sent)

#takes tweets frrom getoldtweets as input
def classify(tweets):
	pos,neg = 0,0
	all_tweets_str=''
	with graph.as_default():
		set_session(sess)
		for tweet in tweets:
			text = tweet.text
			blob = TextBlob(text)
			subjectivity=blob.sentiment.subjectivity
			pred = predict([text])[0][0]
			if pred > 0.5:
				pos+=subjectivity
			elif pred<=0.5:
				neg+=subjectivity
			all_tweets_str += ' ' + tweet.text
			#print('\n\n',tweet.text,pred)
	frequent_words = get_frequent_words(all_tweets_str)
	return {'pos_percentage':100.0*pos/(pos+neg),
			'frequent_words': frequent_words
	}

stop_words = set(stopwords.words('english'))

def get_frequent_words(words_str, top=150):
	tokens = word_tokenize(words_str.lower())
	#tokenList = [token for token in tokenList if re.match('^([a-zA-Z]+|\d+|\W)$', token)]
	filtered_sentence = [w for w in tokens if not w in list(stop_words)+list(string.punctuation)+list('”“’') and  re.match('^([a-zA-Z]+|\d+|\W)$', w)]
	counter =  Counter(filtered_sentence)
	return counter.most_common(top+1)[1:]