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
  movie_str = '&s=Dil Dhadakne Do'
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
  for d in dtags:
    listofreviews.append(d.text.strip())

  #print(listofreviews)
  for str in listofreviews:
    startindex=str.find('Favorite films:')
    cleanedstr=str[0:startindex]
    cleanedreviews.append(cleanedstr)
    #print("Start is",startindex)
  print("Cleaned Reviews",cleanedreviews)
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
