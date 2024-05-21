from django.shortcuts import render
from .forms import AnimeSearch

import re

from pynimeapi import PyNime
pynime = PyNime()

class AnimeData:
    def __init__(self, title, category_url="", latest_episode_int="", latest_episode_url="", picture_url=""):
        self.title = title
        self.category_url = category_url
        self.latest_episode_int = latest_episode_int
        self.latest_episode_url = latest_episode_url
        self.picture_url = picture_url

# Create your views here.
def index(request):
    anime_data_list = list()
    recent_anime = pynime.get_recent_release()

    for i in recent_anime:
        anime_data_list.append(
            AnimeData(
                title=i.title,
                latest_episode_int=i.latest_episode,
                latest_episode_url=i.latest_episode_url.replace(pynime.baseURL,""),
                picture_url=i.picture_url,
            )
        )

    context = {
        'anime_data_list': anime_data_list,
    }
    return render(request, 'animestreaming/index.html', context)

async def watch(request, anime_episode_url: str, video_res: int):
    stream_url = pynime.get_stream_urls(f"{pynime.baseURL}/{anime_episode_url}")[str(video_res)]
    episode = re.findall(r"episode-(\d+)", anime_episode_url)[0]
    anime_title = pynime.search_anime(
        re.findall(r"(\S*)-episode", anime_episode_url)[0]
    )[0].title
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
            anime_result_list = list()
            anime_search_query = form.cleaned_data['search_query']
            search_result = pynime.search_anime(anime_search_query)

            for i in search_result:
                anime_result_list.append(
                    AnimeData(
                        title=i.title,
                        category_url=re.findall(r"\S*category/(\S*)", i.category_url)[0],
                        picture_url=i.picture_url,
                    )
                )

            context = {
                'search_query': anime_search_query,
                'search_result': anime_result_list,
            }
            return render(request, 'animestreaming/search.html', context)

    return render(request, 'animestreaming/search.html', {'search_result': []})

def details(request, anime_category_url: str):
    anime_details = (pynime.get_anime_details(f"{pynime.baseURL}/category/{anime_category_url}"))
    get_episodes = (pynime.get_episode_urls(f"{pynime.baseURL}/category/{anime_category_url}"))

    context = {
        'anime_watch_url': anime_category_url,
        'anime_title': anime_details.title,
        'anime_synopsis': anime_details.synopsis,
        'anime_picture_url': anime_details.image_url,
        # 'anime_genres': ", ".join(str(genre) for genre in anime_details.genres),
        'anime_genres': '',
        'anime_status': anime_details.status,
        'anime_season': anime_details.season,
        'total_episode': len(get_episodes),
        'list_episodes': get_episodes,
    }
    return render(request, 'animestreaming/details.html', context)