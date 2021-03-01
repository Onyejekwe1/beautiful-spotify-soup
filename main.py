from bs4 import BeautifulSoup as b
import requests as r
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

play_list_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

URL = f"https://www.billboard.com/charts/hot-100/{play_list_date}"

response = r.get(URL).text

soup = b(response, "html.parser")

playlists = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
# print(playlists)

playlists_titles = [playlist.getText() for playlist in playlists]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               scope="playlist-modify-private",
                                               redirect_uri="http://example.com",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               client_secret="YOUR_CLIENT_SECRET"))

user_id = sp.current_user()["id"]
song_uris = []
year = play_list_date.split("-")[0]
for song in playlists_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{play_list_date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist["id"], song_uris)
