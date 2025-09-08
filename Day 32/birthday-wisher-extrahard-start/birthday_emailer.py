from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Optional
import pandas as pd
import random
import smtplib
import os
from dotenv import load_dotenv
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BirthdayEmailer:
    """誕生日メール送信クラス"""

    def __init__(self):
        """環境変数を読み込み、設定を初期化"""
        load_dotenv()
        self.email_address = os.getenv("TEST_MAIL1", "")
        self.password = os.getenv("PASSWORD1", "")
        self.recipient_email = os.getenv("TEST_MAIL2", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        self._validate_env_variables()

    def _validate_env_variables(self) -> None:
        """環境変数が設定されているかチェック"""
        if not all([self.email_address, self.password, self.recipient_email]):
            raise ValueError("必要な環境変数が設定されていません: TEST_MAIL1, PASSWORD1, TEST_MAIL2")

    def load_birthdays(self, csv_path: str = "birthdays.csv") -> Dict[Tuple[int, int], pd.Series]:
        """CSVファイルから誕生日データを読み込む

        Args:
            csv_path: CSVファイルのパス

        Returns:
            誕生日辞書 {(月, 日): 行データ}
        """
        try:
            data = pd.read_csv(csv_path)
            birthday_dict = {}

            for index, row in data.iterrows():
                # より明確な列指定（列名が分からない場合の安全な処理）
                if len(row) >= 5:
                    month = int(row.iloc[3])
                    day = int(row.iloc[4])
                    birthday_dict[(month, day)] = row
                else:
                    logger.warning(f"行 {index} のデータが不完全です")

            logger.info(f"{len(birthday_dict)}件の誕生日データを読み込みました")
            return birthday_dict

        except FileNotFoundError:
            logger.error(f"ファイルが見つかりません: {csv_path}")
            return {}
        except Exception as e:
            logger.error(f"誕生日データの読み込みに失敗しました: {e}")
            return {}

    def get_today_tuple(self) -> Tuple[int, int]:
        """今日の日付を(月, 日)のタプルで取得"""
        today = datetime.now()
        return (today.month, today.day)

    def load_letter_template(self, template_dir: str = "letter_templates") -> Optional[str]:
        """ランダムな手紙テンプレートを読み込む

        Args:
            template_dir: テンプレートディレクトリのパス

        Returns:
            テンプレート内容、読み込み失敗時はNone
        """
        template_path = Path(template_dir) / f"letter_{random.randint(1, 3)}.txt"

        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"テンプレートファイルが見つかりません: {template_path}")
            return None
        except Exception as e:
            logger.error(f"テンプレートファイルの読み込みに失敗しました: {e}")
            return None

    def personalize_message(self, template: str, person_data: pd.Series) -> str:
        """メッセージをパーソナライズする

        Args:
            template: メッセージテンプレート
            person_data: 誕生日の人のデータ

        Returns:
            パーソナライズされたメッセージ
        """
        # nameカラムが存在するかチェック
        if "name" in person_data:
            name = str(person_data["name"])
        else:
            # nameカラムがない場合は最初のカラムを使用
            name = str(person_data.iloc[0]) if len(person_data) > 0 else "Unknown"

        return template.replace("[NAME]", name)

    def send_email(self, subject: str, message: str) -> bool:
        """メールを送信する

        Args:
            subject: メールの件名
            message: メール本文

        Returns:
            送信成功時True、失敗時False
        """
        try:
            with smtplib.SMTP(self.smtp_server, port=self.smtp_port) as connection:
                connection.starttls()
                connection.login(user=self.email_address, password=self.password)

                email_message = f"Subject:{subject}\n\n{message}"
                connection.sendmail(
                    from_addr=self.email_address,
                    to_addrs=self.recipient_email,
                    msg=email_message
                )

            logger.info("メールを正常に送信しました")
            return True

        except smtplib.SMTPException as e:
            logger.error(f"メール送信に失敗しました (SMTP): {e}")
            return False
        except Exception as e:
            logger.error(f"メール送信に失敗しました: {e}")
            return False

    def check_and_send_birthday_emails(self) -> None:
        """今日が誕生日の人がいるかチェックし、該当者にメールを送信"""
        birthday_dict = self.load_birthdays()
        if not birthday_dict:
            logger.info("誕生日データがありません")
            return

        today_tuple = self.get_today_tuple()
        logger.info(f"今日の日付: {today_tuple[0]}月{today_tuple[1]}日")

        if today_tuple in birthday_dict:
            birthday_person = birthday_dict[today_tuple]
            logger.info(f"今日は誕生日の人がいます: {birthday_person.get('name', 'Unknown')}")

            # テンプレートを読み込み
            template = self.load_letter_template()
            if template is None:
                logger.error("テンプレートの読み込みに失敗しました")
                return

            # メッセージをパーソナライズ
            personalized_message = self.personalize_message(template, birthday_person)

            # メールを送信
            success = self.send_email("Happy Birthday!", personalized_message)
            if success:
                logger.info("誕生日メールを送信しました")
            else:
                logger.error("誕生日メールの送信に失敗しました")
        else:
            logger.info("今日は誕生日の人はいません")


def main():
    """メイン処理"""
    try:
        emailer = BirthdayEmailer()
        emailer.check_and_send_birthday_emails()
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
