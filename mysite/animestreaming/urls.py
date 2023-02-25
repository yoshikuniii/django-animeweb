from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('watch/<str:anime_title>/<int:episode>/<int:video_res>', views.watch, name='watch'),
	path('search', views.search_anime, name='search_anime'),
]