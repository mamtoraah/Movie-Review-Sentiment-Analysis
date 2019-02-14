from django.urls import path, include
from . import views
#from django.contrib.auth.views import login, logout

app_name = 'MovieReviewApp'
urlpatterns = [
  path('', views.home_view, name='home'),
  path('graph/', views.graph_view, name='graph')
]