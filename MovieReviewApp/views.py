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
  tmdb.API_KEY ='key lelena mere paas se'
  movie = tmdb.Movies(603)
  print(movie)
  response=movie.info()
  response1=movie.reviews()
  print(response1)
  return render(request, 'MovieReviewApp/home.html', {'data': response1})