from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('watch/<str:anime_episode_url>/<int:video_res>', views.watch, name='watch'),
	path('search', views.search_anime, name='search_anime'),
	path('details/<str:anime_category_url>', views.details, name='details'),
]