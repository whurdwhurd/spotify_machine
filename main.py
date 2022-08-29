from bs4 import BeautifulSoup
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = ClientID
SPOTIPY_CLIENT_SECRET = ClientSecret
SPOTIPY_CLIENT_URI = "https://example.com/callback/"
SCOPE = "playlist-modify-private"

uris = []

date = input("When do you want to travel to?")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
bill = response.text


soup = BeautifulSoup(bill, "html.parser")

titles = soup.select(selector="li ul li h3")
song_names = [re.sub(r'[^A-Za-z0-9 ]+', '', item.getText())for item in titles]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_CLIENT_URI, scope = SCOPE, cache_path='.cache.txt'))

user_id = sp.current_user()["id"]

for title in song_names:
    try:
        results1 = sp.search(q=f"track: {title} year: {date[0:4]}", type="track")
        uri = results1["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError: 
        pass    

response = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

playlist_id1 = response["id"]

sp.playlist_add_items(playlist_id=playlist_id1, items=uris, position=None)
