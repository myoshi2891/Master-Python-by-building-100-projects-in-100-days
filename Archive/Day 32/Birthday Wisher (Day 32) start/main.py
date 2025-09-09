import smtplib
from dotenv import load_dotenv
import os
import datetime as dt
import random

# .env をロード
load_dotenv()

# 環境変数として取得
mail_address = os.getenv("TEST_MAIL1", "")
my_mail = os.getenv("TEST_MAIL2", "")
password1 = os.getenv("PASSWORD1", "")

now = dt.datetime.now()
day_of_weekday = now.weekday()
if day_of_weekday == 0:
    with open("quotes.txt") as file:
        all_quotes = file.readlines()
        quote_of_the_day = random.choice(all_quotes)
    print(quote_of_the_day)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=mail_address, password=password1)
        connection.sendmail(
            from_addr=mail_address,
            to_addrs=mail_address,
            msg=f"Subject:Monday Motivation\n\n{quote_of_the_day}",
        )


# # 必要な環境変数が設定されているかチェック
# if not mail_address or not my_mail or not password1:
#     raise ValueError("必要な環境変数が設定されていません。.envファイルを確認してください。")

# with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
#     connection.starttls()
#     connection.login(user=mail_address, password=password1)
#     connection.sendmail(
#         from_addr=mail_address,
#         to_addrs=my_mail,
#         msg="Subject:Hello text again!\n\nThis is the body of my email.",
#     )


# 現在の日時を表示
# year = now.year
# month = now.month
# day = now.day
# hour = now.hour
# minute = now.minute
# second = now.second
# print("Current date:", year, "/", month, "/", day, " (Weekday:", weekday, ")")
# print("Current time:", hour, ":", minute, ":", second)
# print("Current date and time:", now)

# date_of_birth = dt.datetime(year=1996, month=5, day=21, hour=15)
# print("My birthday:", date_of_birth)
# print("Birthday weekday:", date_of_birth.weekday())
