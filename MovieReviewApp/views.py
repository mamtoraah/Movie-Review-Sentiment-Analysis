from django.shortcuts import render
import requests
import tmdbsimple as tmdb
from MovieReviewApp.key import apikey
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
##from sklearn.feature_extraction.text import CountVectorizer
'''
Dil Dhadakne Do : 0.18812277897014912 25 
Dangal : avg:  0.2529289888262045  count:  25
Deadpool : avg:  0.1209913874006312  count:  25
'''
#import scrapy

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
  reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
  reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
  return reviews

# def scrape():
#   temp = scrapy.fetch("https://www.reddit.com/r/gameofthrones/")
#   print(temp)

# Create your views here.
def home_view(request):
  key = apikey
  movie_str = '&s=DeadPool'
  url = 'http://www.omdbapi.com/?apikey=' + apikey + movie_str
  response = requests.get(url)
  data = response.json()
  id = data['Search'][0]['imdbID']
  print("IMDBID:", id)
  page = requests.get('https://www.imdb.com/title/'+id+'/reviews?ref_=tt_urv')
  soup = BeautifulSoup(page.text, 'html.parser')
  #print(soup.prettify())
  dtags = soup.find_all("div", { "class" : "text show-more__control" })
  #print("d tags are",dtags)

  listofreviews=[]
  cleanedreviews=[]
  preprocessedreviews = []
  for d in dtags:
    listofreviews.append(d.text.strip())

  #print(listofreviews)
  for str in listofreviews:
    startindex=str.find('Favorite films:')
    cleanedstr=str[0:startindex]
    cleanedreviews.append(cleanedstr)
    #print("Start is",startindex)
  sentiment = 0.0
  count = 0
  for s in cleanedreviews:
    preprocessedreviews.append(preprocess_reviews(s))
    count += 1
    blob_object = TextBlob(s)
    sentiment += blob_object.sentiment.polarity
    print(sentiment)

  print("avg: ", sentiment/count, " count: ", count)    
  values={'Sentiment Rating from TMDB API':8.5,'Sentiment Rating from Web Scraper':7.5,'Actual Rating':6.2,'Proposed Rating':6.8}
  return render(request, 'MovieReviewApp/home.html', {'data': values})

#def home_view(request):
#  tmdb.API_KEY ='784b4dff6c62ccbe711abb6b8163979f'
#  search = tmdb.Search()
#  id = search.movie(query='Dangal')['results'][0]['id']
#  print(id)
#  movie = tmdb.Movies(id)
#  print(movie.info())
#  #print(movie.reviews())
#  response1=movie.reviews()
#  data = response1['results'][0]['content']
#  print(data)
#  return render(request, 'MovieReviewApp/home.html', {'data': 1})
