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

REPLACE_NO_SPACE = re.compile(
    "(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)|(\\r)|(\\n)")


def preprocess_reviews(reviews):
  reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
  reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
  return ''.join(reviews)


def scrape():
  temp = scrapy.fetch("https://www.reddit.com/r/gameofthrones/")
  print(temp)

# Create your views here.

def list_view(request):
  movie_name_query = "deadpool"
  filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
  with open(filename) as json_file:
    temp = json.load(json_file)

  mylist = []
  newlist = []
  for i in temp['movie']:
      if (i['movie_name'] == movie_name_query):
        mylist = i['review']
  for i in mylist:
    k = i[0:200]
    newlist.append(k)
  return render(request, 'MovieReviewApp/list.html', {'mylist': newlist})

def graph_view(request):
  values = {
              'Sentiment Rating from TMDB API': 10,
              'Sentiment Rating from Web Scraper': 8,
              'Actual Rating': 6.2,
              'Proposed Rating': 6.8
          }
  data = ''
  if request.method == 'POST':
    key = apikey
    movie_name = request.POST.get('search_movie')

    filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
    with open(filename) as json_file:
      temp = json.load(json_file)

    t = movie_name.replace(" ", "").lower()
    for i in temp['movie']:
      if (i['movie_name'] == t):
        values = {
            'Sentiment Rating from TMDB API': i['tmdb_rating'],
            'Sentiment Rating from Web Scraper': i['sentiment'],
            'Actual Rating': 6.2,
            'Proposed Rating': 6.8
        }
        return render(request, 'MovieReviewApp/graph.html', {'data': values})
    movie_str = '&s=' + movie_name
    # http://www.omdbapi.com/?apikey=404e7523&s=The Shawshank Redemption
    url = 'http://www.omdbapi.com/?apikey=' + apikey + movie_str
    response = requests.get(url)
    data = response.json()
    id = data['Search'][0]['imdbID']

    rating = data['Search'][0]

    print("IMDBID:", id)
    page = requests.get('https://www.imdb.com/title/' +
                        id+'/reviews?ref_=tt_urv')
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.prettify())
    dtags = soup.find_all("div", {"class": "text show-more__control"})
    #print("d tags are",dtags)

    listofreviews = []
    cleanedreviews = []
    preprocessedreviews = []
    for d in dtags:
      listofreviews.append(d.text.strip())

    # print(listofreviews)
    for str in listofreviews:
      startindex = str.find('Favorite films:')
      cleanedstr = str[0:startindex]
      cleanedreviews.append(cleanedstr)
      #print("Start is",startindex)
    
    import pickle
    from sklearn.externals import joblib
    model = os.path.dirname(os.path.realpath(__file__)) + '/model_random_forest.pkl'
    loaded_model = joblib.load(model)
    ngram_vectorizer = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '/ngram_3.pkl', 'rb'))

    sentiment = 0.0
    new_model_sentiment = 0.0
    count = 0
    for s in cleanedreviews:
      preprocessedreviews.append(preprocess_reviews(s))
      count += 1
      blob_object = TextBlob(s)
      sentiment += blob_object.sentiment.polarity
      transformed = ngram_vectorizer.transform([s])
      klass = loaded_model.predict(transformed)
      ttemp = loaded_model.predict_proba(transformed)
      print(klass, ttemp)
      if klass == 0:
        curr_sent = loaded_model.predict_proba(transformed)[0, 0]
        new_model_sentiment += -( curr_sent + 0.48 )/ (0.52 - 0.48) #minmax norm
      else:
        curr_sent = loaded_model.predict_proba(transformed)[0, 1]
        new_model_sentiment += ( curr_sent - 0.48 )/ (0.52 - 0.48) #minmax norm
      #curr_sent = 1
      new_model_sentiment += ( curr_sent - 0.48 )/ (0.52 - 0.48) #minmax norm
      print(sentiment," new sent: " , new_model_sentiment)
      data = sentiment/count
    print("avg: ", data, " count: ", count)

    # preprocessedreviews is a list of reviews on which the sentiment analysis 
    # is applied.
    # save the preprocessed reviews in a file named : data.json
    # structure : 
    # {moviename : {review : [reviews], sentiment : value, tmdb_rating}
    movie = movie_name.replace(" ", "").lower()
    tmdb.API_KEY = '521b67c3f5ed3c1369247d6bf7592c00'
    search = tmdb.Search()
    #avgvote = search.movie(query=movie_name)['results'][0]['vote_average']
    #print("Avg vote is ", avgvote)
    #tmdb_rating = avgvote
    tmdb_id = search.movie(query=movie_name)['results'][0]['id']
    _movie = tmdb.Movies(id)
    response1 = _movie.reviews()
    tmdb_review = response1['results'][0]['content']
    print(tmdb_review.lower())
    tmdb_preprocessed = preprocess_reviews(tmdb_review)
    print(tmdb_preprocessed)
    tmdb_blob_object = TextBlob(tmdb_preprocessed)
    tmdb_sentiment = blob_object.sentiment.polarity
    print(tmdb_sentiment)
    
    #pydict to store in the database: data.json
    pydict = {
        'movie_name': movie,
        'review': preprocessedreviews,
        'sentiment': data,
        'tmdb_review' : tmdb_preprocessed,
        'tmdb_rating': tmdb_sentiment,
        'trained_model_rating': new_model_sentiment
    }

    temp['movie'].append(pydict)

    with open(filename, 'w') as f:
      json.dump(temp, f)

    # sourcelist = []
    # ratelist = []
    # urlrating = 'http://www.omdbapi.com/?apikey=' + \
    #     apikey+'&i='+id+'&plot=short&r=json&tomatoes=true'
    # responserating = requests.get(urlrating)
    # datarating = responserating.json()
    # print("datarating is", datarating)
    # ratingarray = datarating['Ratings']
    # for x in ratingarray:
    #   source = x['Source']
    #   rating = x['Value']
    #   sourcelist.append(source)
    #   ratelist.append(rating)
    # print("Source list is ", sourcelist)
    # print("Rating is ", ratelist)

    #values to display
    values = {
              'Sentiment Rating from TMDB API': tmdb_sentiment,
              'Sentiment Rating from Web Scraper': data,
              'Actual Rating': 6.2,
              'Proposed Rating': 6.8
          }
  return render(request, 'MovieReviewApp/graph.html', {'data': values})


# def graph_view(request):
#   data = ''
#   if request.method == 'POST':
#     key = apikey
#     movie_name = request.POST.get('search_movie')
#     print("Movie name is =", movie_name)
#     filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
#     with open(filename) as json_file:
#       temp = json.load(json_file)

#     t = movie_name.replace(" ", "").lower()
#     for i in temp['movie']:
#       if (i['movie_name'] == t):
#         return render(request, 'MovieReviewApp/graph.html', {'data': i['sentiment']})

#     movie_str = '&s=' + movie_name
#     print("Movie name  is :", movie_str)
#   print('hello this is from graph view')
#   values = {'Sentiment Rating from TMDB API': 8.5,
#             'Sentiment Rating from Web Scraper': 7.5, 'Actual Rating': 6.2, 'Proposed Rating': 6.8}
#   return render(request, 'MovieReviewApp/graph.html', {'data': values})

# hemal's key : 521b67c3f5ed3c1369247d6bf7592c00
# jinay's key : 784b4dff6c62ccbe711abb6b8163979f


def home_view(request):
  # tmdb.API_KEY = '521b67c3f5ed3c1369247d6bf7592c00'
  # search = tmdb.Search()
  # avgvote = search.movie(query='Dangal')['results'][0]['vote_average']
  # print("Avg vote is ", avgvote)
  # popularity = search.movie(query='Dangal')['results'][0]['popularity']
  # print("popularity is ", popularity)
  # id = search.movie(query='Dangal')['results'][0]['id']
  # print("The id is", id)
  # movie = tmdb.Movies(id)

  # # print(movie.reviews())
  # response1 = movie.reviews()
  # data = response1['results'][0]['content']
  #print(data)
  return render(request, 'MovieReviewApp/home.html', {'data': 1})