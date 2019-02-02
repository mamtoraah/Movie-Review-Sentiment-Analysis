from django.shortcuts import render
import requests
from MovieReviewApp.key import apikey

# Create your views here.
def home_view(request):
  key = apikey
  url = 'http://www.omdbapi.com/?i=tt3896198&apikey=' + apikey
  response = requests.get(url)
  data = response.json()
  return render(request, 'MovieReviewApp/home.html', {'data': data})
