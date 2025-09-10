# * **定数の整理**: メールアドレス、座標などを定数化
# * **例外処理追加**: `requests` や SMTP での通信失敗時をハンドリング
# * **責務の分離**: 「ISS 判定」「昼夜判定」「通知処理」「ループ処理」を関数に分ける
# * **戻り値の明確化**: `is_iss_overhead` / `is_night` が `bool` を返すように修正
# * **読みやすい構造**: `main()` を導入

# リファクタ済みコードを示します👇

# ```python
import os
import time
import smtplib
import requests
from datetime import datetime
from dotenv import load_dotenv

# -----------------------------
# 定数
# -----------------------------
TOKYO_LAT = 35.6895
TOKYO_LNG = 139.6917
CHECK_INTERVAL = 360  # 分ごとにチェック

ISS_API_URL = "http://api.open-notify.org/iss-now.json"
SUN_API_URL = "https://api.sunrise-sunset.org/json"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# -----------------------------
# 環境変数読み込み
# -----------------------------
load_dotenv()
EMAIL_ADDRESS = os.getenv("TEST_MAIL1", "")
EMAIL_PASSWORD = os.getenv("PASSWORD1", "")


# -----------------------------
# ISS が頭上にあるかどうか判定
# -----------------------------
def is_iss_overhead(lat: float, lng: float) -> bool:
    try:
        response = requests.get(ISS_API_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] ISS API request failed: {e}")
        return False

    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    return (lat - 5) <= iss_lat <= (lat + 5) and (lng - 5) <= iss_lng <= (lng + 5)


# -----------------------------
# 現在が夜かどうか判定
# -----------------------------
def is_night(lat: float, lng: float) -> bool:
    params = {"lat": lat, "lng": lng, "formatted": 0}

    try:
        response = requests.get(SUN_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Sunrise-Sunset API request failed: {e}")
        return False

    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    current_hour = datetime.utcnow().hour  # API が UTC を返すので合わせる
    return current_hour >= sunset_hour or current_hour <= sunrise_hour


# -----------------------------
# メール送信処理
# -----------------------------
def send_email(subject: str, body: str, to_addr: str) -> None:
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("[ERROR] Missing email credentials.")
        return

    try:
        with smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=to_addr,
                msg=f"Subject:{subject}\n\n{body}",
            )
        print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


# -----------------------------
# メイン処理
# -----------------------------
def main():
    print("[INFO] ISS Tracker started.")
    while True:
        time.sleep(CHECK_INTERVAL)
        if is_iss_overhead(TOKYO_LAT, TOKYO_LNG) and is_night(TOKYO_LAT, TOKYO_LNG):
            send_email(
                subject="Look Up👆",
                body="The ISS is above you in the sky.",
                to_addr=EMAIL_ADDRESS,
            )


if __name__ == "__main__":
    main()
# ```

# ---

# ### 改善ポイントまとめ

# * **API通信失敗時** → エラーを握り潰さず `print` で通知
# * **戻り値の統一** → `is_iss_overhead` / `is_night` が必ず `bool` を返す
# * **UTC に統一** → `datetime.utcnow()` を利用（sunrise-sunset API は UTC 基準）
# * **main() 関数導入** → スクリプトのエントリーポイントを明確化

