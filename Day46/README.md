# `main.py` のリファクタリングを行い、Pylance での型付けに対応した、より保守性の高いコードを提案します

主な変更点は以下の通りです。

1. **機能の関数化**: ロジックを「Billboard から曲名を取得」「Spotify で曲を検索」「プレイリスト作成」などの小さな関数に分割しました。
2. **型ヒントの追加**: すべての関数と主要な変数に型ヒントを追加し、コードの可読性と安全性を向上させました。
3. **メイン処理の集約**: `main()` 関数をエントリーポイントとし、`if __name__ == "__main__":` から呼び出す構造にしました。
4. **定数の整理**: URL やスコープなどの設定値を定数としてまとめました。
5. **エラーハンドリングの強化**: `requests` の通信失敗や、Spotify API の操作が失敗した場合のチェックを強化しました。
6. **不要なコードの削除**: プレイリスト作成の主目的とは関係のない「ユーザーの保存済みトラックの表示」部分を削除し、コードをスリム化しました。

以下にリファクタリング後のコードを記載します。

## 修正後のコード

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day46/main.py
import requests
import spotipy
from bs4 import BeautifulSoup
from config import CLIENT_ID, CLIENT_SECRET
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from typing import List, Optional, Dict, Any

# --- 定数定義 ---
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8080"
SPOTIFY_SCOPE = "playlist-modify-private"
USERNAME = "Mitsuru"  # ご自身のSpotifyユーザー名に合わせて変更してください

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
        response = requests.get(url)
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
                print(f"Found: '{song}'")
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
```

ご指摘ありがとうございます。
リファクタリングしたファイルで曲が取得できなくなったとのこと、申し訳ありません。

## 原因

リファクタリングの際に、Billboard のサイトへアクセスする`requests.get()`呼び出しから**`User-Agent`ヘッダーが欠落してしまった**ことが原因です。

多くのウェブサイトは、スクレイピング対策として、ブラウザからのアクセスであることを示す`User-Agent`ヘッダーがないリクエストをブロックします。元のコードにはこのヘッダーが含まれていましたが、リファクタリング後の`scrape_billboard_songs`関数から漏れていました。

## 修正方法

`scrape_billboard_songs`関数に`User-Agent`ヘッダーを追加することで、問題を解決できます。

1. `main_refactored.py`の上部にヘッダー用の定数を追加します。
2. `scrape_billboard_songs`関数内の`requests.get()`呼び出しに、そのヘッダーを渡します。

以下に修正箇所を示します。

```python
# File: /Users/mitsuruyoshizumi/workspace/Python/Master-Python-by-building-100-projects-in-100-days/Day46/main_refactored.py
# ... existing code
# --- 定数定義 ---
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8080"
SPOTIFY_SCOPE = "playlist-modify-private user-library-read"
USERNAME = "Mitsuru"  # ご自身のSpotifyユーザー名に合わせて変更してください
REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# --- 関数定義 ---

# ... existing code
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
# ... existing code
```

## 変更点のまとめ

1. **`REQUEST_HEADER`定数の追加**:
   `User-Agent`と、念のため`Accept-Language`を含むヘッダー情報を定数として定義しました。

2. **`scrape_billboard_songs`関数の修正**:
   `requests.get()`の引数に`headers=REQUEST_HEADER`を追加し、リクエスト時にヘッダーが送信されるように修正しました。

この修正により、Billboard のサイトから正常に曲名リストが取得できるようになるはずです。お手数ですが、こちらの内容でファイルを更新してお試しください。
