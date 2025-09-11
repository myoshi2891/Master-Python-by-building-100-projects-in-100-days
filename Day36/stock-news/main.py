import requests
import os
from dotenv import load_dotenv
# from twilio.rest import Client
load_dotenv()

# 環境変数の取得
STOCK_API = os.getenv("STOCK_API")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
r = requests.get(STOCK_ENDPOINT, params=stock_params)
data = r.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
# print(data_list)

# print(data)
# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
# print(yesterday_closing_price)


# 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
# print(day_before_yesterday_closing_price)

# 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / yesterday_closing_price) * 100)
# print(percentage_difference)

# 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_difference) >= 0:
    # print("Get News")

# 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": os.getenv("NEWS_API"),
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    # print(three_articles)

# 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    articles_titles_and_descriptions = [f"{STOCK_NAME}: {up_down}{percentage_difference}% \n Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(articles_titles_and_descriptions)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.
    # You will need to install the twilio library by running `pip install twilio`.
    # Also, remember to replace "your-phone-number" and "your-auth-token" with your actual phone number and auth token.

    # account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    # auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    # client = Client(account_sid, auth_token)

    # for article in articles_titles_and_descriptions:
    #     message = client.messages.create(
    #         body=article,
    #         from_="your-phone-number",
    #         to="your-phone-number"
    #     )
    #     print(f"SMS sent to {message.to}: {message.body}")

    # formatted_articles = [f"{article['headline']}: {article['description']}" for article in articles[:3]]
    # print(formatted_articles)

#TODO 9. - Send each article as a separate message via Twilio.


#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
