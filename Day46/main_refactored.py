from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import spotipy
from bs4 import BeautifulSoup
from config import CLIENT_ID, CLIENT_SECRET, USERNAME
from spotipy.oauth2 import SpotifyOAuth

# --- 定数定義 ---
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8080"
SPOTIFY_SCOPE = "playlist-modify-private user-library-read"
USERNAME = USERNAME  # ご自身のSpotifyユーザー名に合わせて変更してください
REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# --- 関数定義 ---


def setup_spotify_client() -> spotipy.Spotify:
    """Spotify APIクライアントを認証・設定して返す"""
    token_path = Path(__file__).parent / "token.txt"
    auth_manager = SpotifyOAuth(
        scope=SPOTIFY_SCOPE,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path=str(token_path),
        username=USERNAME,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def get_user_date() -> str:
    """ユーザーから日付の入力を受け付ける"""
    return input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
    )


def scrape_billboard_songs(date: str) -> List[str]:
    """指定された日付のBillboard Hot 100から曲名リストを取得する"""
    url = BILLBOARD_URL + date
    try:
        response = requests.get(url, headers=REQUEST_HEADER)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching Billboard data: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    song_names_spans = soup.select("li ul li h3")
    return [song.get_text(strip=True) for song in song_names_spans]


def get_spotify_uris(
    sp: spotipy.Spotify, song_titles: List[str], year: str
) -> List[str]:
    """曲名リストを元にSpotifyで曲を検索し、URIのリストを返す"""
    song_uris: List[str] = []
    print("\nSearching for songs on Spotify...")
    for song in song_titles:
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
        try:
            if result and result["tracks"]["items"]:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
                # print(f"Found: '{song}'")
            else:
                print(f"Could not find '{song}' on Spotify. Skipping.")
        except (IndexError, KeyError):
            print(f"Error processing search result for '{song}'. Skipping.")
    return song_uris


def create_spotify_playlist(
    sp: spotipy.Spotify, user_id: str, date: str
) -> Optional[Dict[str, Any]]:
    """Spotifyに新しい非公開プレイリストを作成する"""
    playlist_name = f"Billboard Hot 100 - {date}"
    try:
        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_name, public=False
        )
        print(f"\nSuccessfully created playlist: '{playlist_name}'")
        return playlist
    except spotipy.SpotifyException as e:
        print(f"Failed to create playlist: {e}")
        return None


def add_songs_to_playlist(
    sp: spotipy.Spotify, playlist_id: str, song_uris: List[str]
) -> None:
    """指定されたプレイリストに曲を追加する"""
    if not song_uris:
        print("No songs to add.")
        return

    try:
        sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
        print(f"Successfully added {len(song_uris)} songs to the playlist.")
    except spotipy.SpotifyException as e:
        print(f"Failed to add songs to playlist: {e}")


# --- メイン処理 ---


def main() -> None:
    """メインの処理を実行する"""
    sp = setup_spotify_client()

    current_user = sp.current_user()
    if not current_user or "id" not in current_user:
        print("Could not get user information from Spotify. Exiting.")
        return
    user_id = current_user["id"]

    date = get_user_date()
    year = date.split("-")[0]

    song_titles = scrape_billboard_songs(date)
    if not song_titles:
        print("Could not find any songs on Billboard for the given date. Exiting.")
        return

    song_uris = get_spotify_uris(sp, song_titles, year)
    if not song_uris:
        print("No songs were found on Spotify. Exiting.")
        return

    playlist = create_spotify_playlist(sp, user_id, date)
    if playlist and "id" in playlist:
        add_songs_to_playlist(sp, playlist["id"], song_uris)


if __name__ == "__main__":
    main()
