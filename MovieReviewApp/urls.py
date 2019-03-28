from django.urls import path, include
from . import views
from django.conf.urls import url
#from django.contrib.auth.views import login, logout

app_name = 'MovieReviewApp'
urlpatterns = [
  path('', views.home_view, name='home'),
  url(r'^graph/$',views.graph_view,name='graph'),
  #path('/graph', views.graph_view, name='graph')
  url('list/', views.list_view, name='list')

  #path('/<str:>')
]