from django.shortcuts import render
import requests
import tmdbsimple as tmdb
from MovieReviewApp.key import apikey

# Create your views here.
# def home_view(request):
#   key = apikey
#   url = 'http://www.omdbapi.com/?i=tt3896198&apikey=' + apikey
#   response = requests.get(url)
#   data = response.json()
#   return render(request, 'MovieReviewApp/home.html', {'data': data})
def home_view(request):
  tmdb.API_KEY ='784b4dff6c62ccbe711abb6b8163979f'
  search = tmdb.Search()
  id = search.movie(query='Dangal')['results'][0]['id']
  print(id)
  movie = tmdb.Movies(id)
  print(movie.info())
  #print(movie.reviews())
  response1=movie.reviews()
  data = response1['results'][0]['content']
  print(data)
  return render(request, 'MovieReviewApp/home.html', {'data': 1})
