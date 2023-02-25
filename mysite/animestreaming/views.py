from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .forms import AnimeSearch

from pynimeapi import PyNime
pynime = PyNime()

# Create your views here.
def index(request):
    anime_data_list = pynime.get_recent_release()
    # anime_data_list = []
    context = {'anime_data_list': anime_data_list}
    return render(request, 'animestreaming/index.html', context)

def watch(request, anime_title: str, episode: int, video_res: int):
    stream_url = pynime.grab_stream(anime_title=anime_title, episode=episode, resolution=video_res)
    # stream_url = "https://tnc-11.abecdn.com/1ab5d45273a9183bebb58eb74d5722d8ea6384f350caf008f08cf018f1f0566d0cb82a2a799830d1af97cd3f4b6a9a81ef3aed2fb783292b1abcf1b8560a1d1aa308008b88420298522a9f761e5aa1024fbe74e5aa853cfc933cd1219327d1232e91847a185021b184c027f97ae732b3708ee6beb80ba5db6628ced43f1196fe/d0a7559869d315c5498ebe1e346aae43/ep.1.1665240453.720.m3u8"
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