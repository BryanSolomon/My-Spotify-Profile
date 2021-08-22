"""Spotify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Profile.views import get_top_genres, playlists_view, profile_view, recently_played_view, top_artists_view, top_tracks_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', profile_view),
    path('recently-played/', recently_played_view),
    path('top-tracks/', top_tracks_view),
    path('playlists/', playlists_view),
    path('top-artists/', top_artists_view),
    path('api/top-genres/', get_top_genres)
]
