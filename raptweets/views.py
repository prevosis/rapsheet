from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse

from .models import Tweet, Album
from . import engine

def index(request):
    return render_to_response('raptweets/index.html')


# TODO more intelligent search
def search(request):
    query = request.GET.get('album_title')
    if query:
        titles = close_titles()
        if query.lower() in titles:
            title = titles[query.lower()].title
            album = get_object_or_404(Album, title=title)
            return graph(request, album.id)
    return HttpResponse('404')

def tweets(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)  # Query
    query = engine.get_sentiment(engine.search(album.title))
    for tweet in query:
        t = Tweet(text=tweet['text'],
                  sentiment=tweet['sentiment'],
                  pub_date=tweet['date'],
                  album=album)
        try:
            Tweet.objects.get(text=t.text)  # Query
        except(KeyError, Tweet.DoesNotExist):
            t.save()
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    return render(
        request, 'raptweets/tweets.html', {
            'tweets': Tweet.objects.filter(album=album),  # Query
            'album': album,
            'avg': avg
        }
    )

def graph(request, album_id=0):
    album = get_object_or_404(Album, pk=album_id)
    tw = Tweet.objects.filter(album=album)
    if not tw:
        query = engine.get_sentiment(engine.search(album.title))
        for tweet in query:
            t = Tweet(text=tweet['text'],
                      sentiment=tweet['sentiment'],
                      pub_date=tweet['date'],
                      album=album)
            try:
                Tweet.objects.get(text=t.text)
            except(KeyError, Tweet.DoesNotExist):
                t.save()
    avg = engine.average_sentiment_per_day(Tweet.objects.filter(album=album))  # Query
    for key in avg:
        avg[key] = "%.2f" % avg[key]
    import json
    return render(request, 'raptweets/graph.html', {
        'album': album,
        'avg': json.dumps(avg)
    })

def close_titles():
    titles = {}
    a = Album.objects.all()
    for i in range(len(a)):
        titles[a[i].title.lower()] = a[i]
    return titles
