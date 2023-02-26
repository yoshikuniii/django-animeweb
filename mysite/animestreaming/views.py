from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .forms import AnimeSearch

from pynimeapi import PyNime
pynime = PyNime()

# Create your views here.
def index(request):
    anime_data_list = pynime.get_recent_release()
    context = {'anime_data_list': anime_data_list}
    return render(request, 'animestreaming/index.html', context)

def watch(request, anime_title: str, episode: int, video_res: int):
    stream_url = pynime.grab_stream(anime_title=anime_title, episode=episode, resolution=video_res)
    context = {
        'anime_title': anime_title,
        'episode': episode,
        'video_source': stream_url,
    }
    return render(request, 'animestreaming/watch.html', context)

def search_anime(request):
    if request.method == 'POST':
        form = AnimeSearch(request.POST)
        if form.is_valid():
            anime_search_query = form.cleaned_data['search_query']
            search_result = pynime.search_anime(anime_search_query)
            return render(request, 'animestreaming/search.html', {'search_result': search_result})

    return render(request, 'animestreaming/search.html', {'search_result': []})

def details(request, anime_title: str):
    anime_data = pynime.search_anime(anime_title)
    anime_details = pynime.get_anime_details(anime_data[0].category_url)
    
    get_episodes = pynime.get_episode_urls(anime_data[0].category_url)

    context = {
        'anime_title': anime_details.title,
        'anime_synopsis': anime_details.synopsis,
        'anime_picture_url': anime_details.image_url,
        'anime_genres': ", ".join(str(genre) for genre in anime_details.genres),
        'anime_status': anime_details.status,
        'anime_season': anime_details.season,
        'total_episode': len(get_episodes),
        'list_episodes': get_episodes,
    }
    return render(request, 'animestreaming/details.html', context)