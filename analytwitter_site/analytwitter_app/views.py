from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

from . import scraper
from . import classifier


# Create your views here.
def tweet_search_view(request):
	request_data = json.loads(request.body)
	search_term =  request_data['search_term']
	top_tweets = request_data['top_tweets']
	tweets = scraper.get_tweets(search_term,top=top_tweets)
	results = classifier.classify(tweets)
	pos_percentage = results['pos_percentage']
	frequent_words = results['frequent_words']
	return JsonResponse({"pos_percentage":pos_percentage,'search_term':search_term,'frequent_words':frequent_words})
