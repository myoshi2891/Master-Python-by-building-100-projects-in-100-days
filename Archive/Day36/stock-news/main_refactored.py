from stock_service import fetch_stock_data
from news_service import fetch_news
# from notifier import send_sms  # Twilioを使う場合

from config import STOCK_NAME


def calculate_percentage_difference(stock_data: dict[str, dict[str, str]]) -> tuple[str, int]:
    data_list = list(stock_data.values())
    yesterday_close = float(data_list[0]["4. close"])
    day_before_close = float(data_list[1]["4. close"])
    difference = yesterday_close - day_before_close
    up_down = "🔺" if difference > 0 else "🔻"
    percentage_diff = round((difference / yesterday_close) * 100)
    return up_down, percentage_diff


def main() -> None:
    stock_data = fetch_stock_data()
    up_down, percentage_diff = calculate_percentage_difference(stock_data)

    if abs(percentage_diff) >= 5:
        articles = fetch_news()
        formatted_messages = [
            f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}\nBrief: {article['description']}"
            for article in articles
        ]
        for msg in formatted_messages:
            print(msg)

        # Twilioで送信する場合
        # send_sms(formatted_messages)


if __name__ == "__main__":
    main()
