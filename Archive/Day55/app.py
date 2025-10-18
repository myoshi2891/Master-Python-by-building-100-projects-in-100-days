import random
import secrets
from flask import Flask, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # セキュアなランダムキーを生成


@app.get("/")
def home():
    """ホームページを表示し、新しいゲームを開始する"""
    # 新しいゲームの開始時にセッションに秘密の数を保存
    if 'secret' not in session:
        session['secret'] = random.randint(0, 9)
        app.logger.info(f"New game started. Secret number is {session['secret']}")
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>"


@app.get("/<int:guess>")
def guess_number(guess):
    """ユーザーの推測を評価し、結果を返す"""
    # ゲームが開始されていない場合は、新しいゲームを開始
    if 'secret' not in session:
        session['secret'] = random.randint(0, 9)
        app.logger.info(f"New game started during guess. Secret number is {session['secret']}")

    secret = session['secret']

    if guess > secret:
        app.logger.info(f"User guessed {guess}, which is too high.")
        return "<h1 style='color: purple'>Too high, try again!</h1>" \
               "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>"
    elif guess < secret:
        app.logger.info(f"User guessed {guess}, which is too low.")
        return "<h1 style='color: orange'>Too low, try again!</h1>" \
               "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>"
    else:
        app.logger.info(f"User guessed {guess} correctly! Starting new game.")
        # 正解したらセッションをクリアして新しいゲームを促す
        session.pop('secret', None)
        return "<h1 style='color: green'>Congratulations! You guessed correctly!</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>" \
               "<p><a href='/'>Play again</a></p>"


if __name__ == "__main__":
    app.run(debug=True)
