
from flask import Flask
import random
from typing import Final

# --- 定数定義 ---
MIN_NUMBER: Final[int] = 0
MAX_NUMBER: Final[int] = 9

# メッセージと画像のURLを定数として管理
TOO_HIGH_MESSAGE: Final[str] = (
    "<h1 style='color: purple'>Too high, try again!</h1>"
    "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>"
)
TOO_LOW_MESSAGE: Final[str] = (
    "<h1 style='color: orange'>Too low, try again!</h1>"
    "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>"
)
CORRECT_MESSAGE: Final[str] = (
    "<h1 style='color: green'>Congratulations! You guessed correctly!</h1>"
    "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>"
)
HOME_MESSAGE: Final[str] = (
    f"<h1>Guess a number between {MIN_NUMBER} and {MAX_NUMBER}</h1>"
    '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" />'
)

# --- アプリケーション設定 ---
app = Flask(__name__)
# 正解の数字を一度だけ生成
correct_number: Final[int] = random.randint(MIN_NUMBER, MAX_NUMBER)
print(f"Correct number (for debugging): {correct_number}")


@app.get("/")
def home() -> str:
    """ホームページを表示します。"""
    return HOME_MESSAGE


@app.get("/<int:guess>")
def guess_number(guess: int) -> str:
    """ユーザーの推測を判定し、結果を返します。"""
    if guess > correct_number:
        return TOO_HIGH_MESSAGE
    elif guess < correct_number:
        return TOO_LOW_MESSAGE
    else:
        return CORRECT_MESSAGE


def main() -> None:
    """アプリケーションをデバッグモードで起動します。"""
    app.run(debug=True)


if __name__ == "__main__":
    main()
