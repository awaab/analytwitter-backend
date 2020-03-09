from django.urls import path
from . import views
app_name = 'analytwitter_app'
urlpatterns = [
path('search/', views.tweet_search_view, name='tweet_search_view'),
]