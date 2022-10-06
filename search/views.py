import requests
from django.shortcuts import render, redirect
from django.conf import settings
from isodate import parse_duration
from .forms import SearchForm
from django.http import HttpResponseRedirect


# Create your views here.

def index(request):
    title, videos, context = 'Search Youtube', [], {}
    if request.method == 'POST':
        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"
        params_for_search = {
            "part": "snippet",
            "q": request.POST['search'],
            "maxResults": 9,
            "type": "video",
            "key": settings.YOUTUBE_DATA_API_KEY,
        }
        r = requests.get(search_url, params=params_for_search)
        video_ids = []
        for video in r.json()['items']:
            video_ids.append(video['id']['videoId'])

        title = params_for_search['q']

        if request.POST['submit'] == 'search':
            params_for_video = {
                "part": "snippet,contentDetails",
                "id": ",".join(video_ids),
                "key": settings.YOUTUBE_DATA_API_KEY,
            }
            r = requests.get(video_url, params=params_for_video)
            results = r.json()['items']
            for result in results:
                video_data = {'title': result['snippet']['title'],
                              'id': result['id'],
                              'url': "https://www.youtube.com/watch?v={}".format(result['id']),
                              'time': '{:02d}:{:02d}'.format(
                                  *divmod(int(parse_duration(
                                      result['contentDetails']['duration']).total_seconds() // 60),
                                          60)),
                              'img': result["snippet"]["thumbnails"]['high']['url']
                              }
                videos.append(video_data)

    context['videos'] = videos
    context['title'] = title

    return render(request, 'youtube_app/index.html', context=context)
