from django.shortcuts import render
import requests
import tmdbsimple as tmdb
from MovieReviewApp.key import apikey
from bs4 import BeautifulSoup
#import scrapy

# def scrape():
#   temp = scrapy.fetch("https://www.reddit.com/r/gameofthrones/")
#   print(temp)

# Create your views here.
def home_view(request):
  key = apikey
  movie_str = '&s=Dangal'
  url = 'http://www.omdbapi.com/?apikey=' + apikey + movie_str
  response = requests.get(url)
  data = response.json()
  id = data['Search'][0]['imdbID']
  print("IMDBID:", id)
  page = requests.get('https://www.imdb.com/title/'+id+'/?ref_=nv_sr_1')
  soup = BeautifulSoup(page.text, 'html.parser')
  print(soup.prettify())
  ptags = soup.find_all('p')
  print("P tags are",ptags)
  for p in ptags:
    print(p)
  return render(request, 'MovieReviewApp/home.html', {'data': data})

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
