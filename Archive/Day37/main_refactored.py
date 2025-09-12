import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from pixela_client import create_pixel, update_pixel, delete_pixel

load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")
USERNAME: Optional[str] = os.getenv("USERNAME")
GRAPH_ID: str = "graph2"


def main() -> None:
    if TOKEN is None or USERNAME is None:
        raise ValueError("環境変数 TOKEN または USERNAME が設定されていません。")

    today = datetime.now()
    print("=== Pixela 学習時間管理 ===")
    print("1: 新規追加 (create)")
    print("2: 更新 (update)")
    print("3: 削除 (delete)")

    choice = input("操作を選んでください (1/2/3): ").strip()

    if choice == "1":
        hours = input("今日の学習時間を入力してください (h): ")
        response = create_pixel(TOKEN, USERNAME, GRAPH_ID, today, hours)
        print("Pixel Creation:", response.text)

    elif choice == "2":
        hours = input("修正後の学習時間を入力してください (h): ")
        response = update_pixel(TOKEN, USERNAME, GRAPH_ID, today, hours)
        print("Pixel Update:", response.text)

    elif choice == "3":
        confirm = input("本当に削除しますか？ (y/n): ").lower()
        if confirm == "y":
            response = delete_pixel(TOKEN, USERNAME, GRAPH_ID, today)
            print("Pixel Delete:", response.text)
        else:
            print("削除をキャンセルしました。")

    else:
        print("無効な選択です。終了します。")


if __name__ == "__main__":
    main()
