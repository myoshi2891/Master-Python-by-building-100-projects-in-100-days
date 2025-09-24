from pathlib import Path

import requests
import spotipy
from bs4 import BeautifulSoup
from config import CLIENT_ID, CLIENT_SECRET, USERNAME
from spotipy.oauth2 import SpotifyOAuth

# token.txtをこのスクリプトと同じディレクトリに保存するためのパスを生成
token_path = Path(__file__).parent / "token.txt"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private user-library-read",
        redirect_uri="http://127.0.0.1:8080",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path=str(token_path),  # Pathオブジェクトを文字列に変換
        username=USERNAME,
    )
)

user_id = None
current_user = sp.current_user()

if current_user:
    user_id = current_user["id"]

date = input(
    "What year you would like to travel to? Type date in this format YYYY-MM-DD: "
)

year = date.split("-")[0]

results = sp.current_user_saved_tracks()
if results:
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        print(idx, track["artists"][0]["name"], " – ", track["name"])

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
url = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.get_text().strip() for song in song_names_spans]
song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", limit=1, type="track")
    # print(result)
    try:
        if result:
            uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"Song '{song}' not found in Spotify. Skipping...")

playlist = sp.user_playlist_create(
    user=user_id, name=f"Billboard Hot 100 {date}", public=False
)

print(f"Created playlist: {playlist}")

if playlist and song_uris:
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
else:
    print("Failed to create or add songs to the playlist.")
