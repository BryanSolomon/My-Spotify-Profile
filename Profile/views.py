from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import uuid
from functions import get_artists, session_cache_path, convert_time
from pprint import pprint
from collections import Counter

# cache folder; holds unique token for each browser
caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def profile_view(request):
    # Application follows Spotify's Authorization Code Flow
    session = request.session

    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']

    if not session.get('uuid', False):
        # Step 1. User is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())
    
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        # Step 3. Recieve access token; redirect to Profile
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token is avaiable
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    # current user
    u = sp.me()
    fa = sp.current_user_followed_artists()
    # pprint(fa)
    followed_artists = 0
    for item in fa['artists']['items']:
        followed_artists += 1
    # user's playlists
    pl = sp.current_user_playlists()
    # pprint(pl)
    playlist_total = pl['total']
    if u['images']:
        pfp = u['images'][0]['url']
    else:
        pfp = None
    user = {
        'display_name': u['display_name'],
        'profile_url': u['external_urls']['spotify'],
        'followers': u['followers']['total'],
        'followed_artists': followed_artists,
        'image_url': pfp,
        'playlists': playlist_total,
    }
    # pprint(user)

    # user's top tracks
    tt = sp.current_user_top_tracks(limit=10, time_range='long_term')
    # pprint(tt)
    top_tracks = []
    for item in tt['items']:
        artists = get_artists(item['artists'])
        song = item['name']
        album = item['album']['name']
        duration = int(item['duration_ms'])
        dur = convert_time(duration)
        art_url = item['album']['images'][2]['url']
        url = item['external_urls']['spotify']
        top_tracks.append({
            'artist': artists, 
            'track': song, 
            'album': album, 
            'duration': dur, 
            'art_url': art_url,
            'url': url
        })

    # user's top artists
    ta = sp.current_user_top_artists(limit=10, time_range='long_term')
    # pprint(ta)
    top_artists = []
    for item in ta['items']:
        top_artists.append({
            'name': item['name'], 
            'image_url': item['images'][2]['url'],
            'url': item['external_urls']['spotify']
        })

    # pprint(request.POST)

    context = {
        'user': user,
        'top_tracks': top_tracks,
        'top_artists': top_artists,
    }
    return render(request, 'profile.html', context)


def recently_played_view(request):
    session = request.session
    # Login if there is no token in cache

    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']

    if not session.get('uuid', False):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    rp = sp.current_user_recently_played()
    # pprint(rp)
    recently_played = []
    for item in rp['items']:
        track = item['track']['name']
        url = item['track']['external_urls']['spotify']
        duration = convert_time(item['track']['duration_ms'])
        artists = get_artists(item['track']['artists'])
        album = item['track']['album']['name']
        album_art = item['track']['album']['images'][2]['url']
        recently_played.append({
            'track': track,
            'url': url,
            'duration': duration,
            'artists': artists,
            'album': album,
            'album_art': album_art
        })

    context = {
        'recently_played': recently_played
    }
    return render(request, "recently-played.html", context)


def top_tracks_view(request):
    session = request.session
    # Login if there is no token in cache
    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']

    if not session.get('uuid', False):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    lt = sp.current_user_top_tracks(limit=50, time_range="long_term")
    # pprint(lt)
    long_term = []
    for item in lt['items']:
        cover = item['album']['images'][0]['url']
        track = item['name']
        artists = get_artists(item['artists'])
        duration = convert_time(item['duration_ms'])
        url = item['external_urls']['spotify']
        album = item['album']['name']
        long_term.append({
            'cover': cover,
            'track': track,
            'artists': artists,
            'duration': duration,
            'url': url,
            'album': album     
        })

    mt = sp.current_user_top_tracks(limit=50, time_range="medium_term")
    medium_term = []
    for item in mt['items']:
        cover = item['album']['images'][0]['url']
        track = item['name']
        artists = get_artists(item['artists'])
        duration = convert_time(item['duration_ms'])
        url = item['external_urls']['spotify']
        album = item['album']['name']
        medium_term.append({
            'cover': cover,
            'track': track,
            'artists': artists,
            'duration': duration,
            'url': url,
            'album': album     
        })

    st = sp.current_user_top_tracks(limit=50, time_range="short_term")
    short_term = []
    for item in st['items']:
        cover = item['album']['images'][0]['url']
        track = item['name']
        artists = get_artists(item['artists'])
        duration = convert_time(item['duration_ms'])
        url = item['external_urls']['spotify']
        album = item['album']['name']
        short_term.append({
            'cover': cover,
            'track': track,
            'artists': artists,
            'duration': duration,
            'url': url,
            'album': album     
        })

    context = {
        'long_term': long_term,
        'medium_term': medium_term,
        'short_term': short_term
    }
    return render(request, "top-tracks.html", context)


def playlists_view(request):
    session = request.session
    # Login if there is no token in cache
    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']

    if not session.get('uuid', False):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    pl = sp.current_user_playlists()
    # pprint(pl)
    playlists = []
    for item in pl['items']:
        if item['images']:
            image = item['images'][0]['url']
        else:
            image = None
        name = item['name']
        owner = item['owner']['display_name']
        id = item['id']
        url = item['external_urls']['spotify']
        playlists.append({
            'image': image,
            'name': name,
            'owner': owner,
            'id': id,
            'url': url
        })

    context = {
        'playlists': playlists
    }
    return render(request, "playlists.html", context)

def top_artists_view(request):
    session = request.session
    # Login if there is no token in cache
    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']
            
    if not session.get('uuid', False):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    lt = sp.current_user_top_artists(limit=25, time_range="long_term")
    # pprint(lt)
    long_term = []
    for item in lt['items']:
        image = item['images'][0]['url'] if item['images'] else None
        name = item['name']
        url = item['external_urls']['spotify']
        long_term.append({
            'image': image,
            'name': name,
            'url': url
        })

    mt = sp.current_user_top_artists(limit=25, time_range="medium_term")
    # pprint(mt)
    medium_term = []
    for item in mt['items']:
        image = item['images'][0]['url'] if item['images'] else None
        name = item['name']
        url = item['external_urls']['spotify']
        medium_term.append({
            'image': image,
            'name': name,
            'url': url
        })

    st = sp.current_user_top_artists(limit=25, time_range="short_term")
    # pprint(st)
    short_term = []
    for item in st['items']:
        image = item['images'][0]['url'] if item['images'] else None
        name = item['name']
        url = item['external_urls']['spotify']
        short_term.append({
            'image': image,
            'name': name,
            'url': url
        })

    context = {
        'long_term': long_term,
        'medium_term': medium_term,
        'short_term': short_term
    }
    return render(request, "top-artists.html", context)

def get_top_genres(request):
    session = request.session
    # Login if there is no token in cache
    if request.POST.get('logout', False):
        if os.path.exists(session_cache_path(session, caches_folder)):
            os.remove(session_cache_path(session, caches_folder))
        if session.get('uuid', False):
            del session['uuid']
            
    if not session.get('uuid', False):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(session, caches_folder))
    scope = "user-read-recently-played user-top-read user-follow-read playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope, cache_handler=cache_handler)

    if request.GET.get("code", False) != False:
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render(request, "login.html", {'auth_url': auth_url})

    sp = spotipy.Spotify(auth_manager=auth_manager)

    data = sp.current_user_top_artists(limit=100, time_range="long_term")
    genres_data = {}
    for item in data['items']:
        for genre in item['genres']:
            if genre in genres_data:
                val = genres_data[genre] +1
                genres_data.update({genre: val})
            else:
                genres_data.update({genre: 1})
    c = Counter(genres_data)
    top = c.most_common(10)
    top_10 = {}
    for i in top:
        top_10.update({i[0]: i[1]})

    return JsonResponse(top_10)