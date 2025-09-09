from datetime import datetime
import pandas as pd
import random
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Get the email address and password from environment variables
email_address = os.getenv("TEST_MAIL1", "")
password = os.getenv("PASSWORD1", "")
my_mail = os.getenv("TEST_MAIL2", "")


# 2. Check if today matches a birthday in the birthdays.csv
today = datetime.now()
today_tuple = (today.month, today.day)

data = pd.read_csv("birthdays.csv")
birthday_dict = {}
for index, row in data.iterrows():
    month = int(row.iloc[3])  # 2番目の列（month）
    day = int(row.iloc[4])  # 3番目の列（day）
    birthday_dict[(month, day)] = row

if today_tuple in birthday_dict:
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        birthday_person = birthday_dict[today_tuple]
        letter_contents = letter_file.read()
        letter_contents = letter_contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email_address, password=password)
        connection.sendmail(
            from_addr=email_address,
            to_addrs=my_mail,
            msg=f"Subject:Happy Birthday!\n\n{letter_contents}",
        )
