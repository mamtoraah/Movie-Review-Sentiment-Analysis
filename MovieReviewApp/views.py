from django.shortcuts import render, redirect
import requests
import tmdbsimple as tmdb
import os
from MovieReviewApp.key import apikey
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import json
##from sklearn.feature_extraction.text import CountVectorizer
'''
Dil Dhadakne Do : 0.18812277897014912 25 
Dangal : avg:  0.2529289888262045  count:  25
Deadpool : avg:  0.1209913874006312  count:  25
The godfather:  0.256149240547238 count:  25
Shawshank redemption: avg:  0.245180390140919  count:  25
'''
#import scrapy

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
  reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
  reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
  return ''.join(reviews)

# def scrape():
#   temp = scrapy.fetch("https://www.reddit.com/r/gameofthrones/")
#   print(temp)

# Create your views here.
# def home_view(request):
#   data = ''
#   if request.method ==  'POST':
#     key = apikey
#     movie_name = request.POST.get('search_movie')
#
#     filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
#     with open(filename) as json_file:
#       temp = json.load(json_file)
#
#     t = movie_name.replace(" ", "").lower()
#     for i in temp['movie']:
#       if (i['movie_name'] == t):
#         return render(request, 'MovieReviewApp/home.html', {'data':i['sentiment']})
#
#     movie_str ='&s=' + movie_name
#     #http://www.omdbapi.com/?apikey=404e7523&s=The Shawshank Redemption
#     url = 'http://www.omdbapi.com/?apikey=' + apikey + movie_str
#     response = requests.get(url)
#     data = response.json()
#     id = data['Search'][0]['imdbID']
#     print("IMDBID:", id)
#     page = requests.get('https://www.imdb.com/title/'+id+'/reviews?ref_=tt_urv')
#     soup = BeautifulSoup(page.text, 'html.parser')
#     #print(soup.prettify())
#     dtags = soup.find_all("div", { "class" : "text show-more__control" })
#     #print("d tags are",dtags)
#
#     listofreviews=[]
#     cleanedreviews=[]
#     preprocessedreviews = []
#     for d in dtags:
#       listofreviews.append(d.text.strip())
#
#     #print(listofreviews)
#     for str in listofreviews:
#       startindex=str.find('Favorite films:')
#       cleanedstr=str[0:startindex]
#       cleanedreviews.append(cleanedstr)
#       #print("Start is",startindex)
#     sentiment = 0.0
#     count = 0
#     for s in cleanedreviews:
#       preprocessedreviews.append(preprocess_reviews(s))
#       count += 1
#       blob_object = TextBlob(s)
#       sentiment += blob_object.sentiment.polarity
#       print(sentiment)
#       data = sentiment/count
#     print("avg: ", data, " count: ", count)
#
#     #preprocessedreviews is a list of reviews on which the sentiment analysis is applied.
#     #save the preprocessed reviews in a file named : data.json
#     #structure : {moviename : {review : [reviews], sentiment : value}
#     movie = movie_name.replace(" ", "").lower()
#     pydict = {'movie_name': movie, 'review':preprocessedreviews, 'sentiment': data}
#
#     temp['movie'].append(pydict)
#
#     with open(filename, 'w') as f:
#       json.dump(temp, f)
#
#     sourcelist=[]
#     ratelist=[]
#     urlrating = 'http://www.omdbapi.com/?apikey='+apikey+'&i='+id+'&plot=short&r=json&tomatoes=true'
#     responserating = requests.get(urlrating)
#     datarating = responserating.json()
#     print("datarating is",datarating)
#     ratingarray=datarating['Ratings']
#     for x in ratingarray:
#       source=x['Source']
#       rating=x['Value']
#       sourcelist.append(source)
#       ratelist.append(rating)
#     print("Source list is ",sourcelist)
#     print("Rating is ",ratelist)
#
#
#
#   return render(request, 'MovieReviewApp/home.html', {'data':data})



def graph_view(request):
  print('hello this is from graph view')
  values={'Sentiment Rating from TMDB API':8.5,'Sentiment Rating from Web Scraper':7.5,'Actual Rating':6.2,'Proposed Rating':6.8}
  return render(request, 'MovieReviewApp/graph.html', {'data': values})


def home_view(request):
 tmdb.API_KEY ='784b4dff6c62ccbe711abb6b8163979f'
 search = tmdb.Search()
 avgvote=search.movie(query='Dangal')['results'][0]['vote_average']
 print("Avg vote is ",avgvote)
 popularity = search.movie(query='Dangal')['results'][0]['popularity']
 print("popularity is ",popularity)
 id = search.movie(query='Dangal')['results'][0]['id']
 print("The id is",id)
 movie = tmdb.Movies(id)

 #print(movie.reviews())
 response1=movie.reviews()
 data = response1['results'][0]['content']
 print(data)
 return render(request, 'MovieReviewApp/home.html', {'data': 1})
