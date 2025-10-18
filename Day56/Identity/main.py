from flask import Flask, render_template, request

app = Flask(__name__)

# サイトのコンテンツデータを一元管理
SITE_DATA = {
    "title": "Identity of John Doe",
    "name": "John Doe",
    "role": "Senior Psychonautics Engineer",
    "avatar": "images/avatar.jpg",
    "social_links": [
        {"name": "Twitter", "url": "#", "icon": "fa-twitter"},
        {"name": "Instagram", "url": "#", "icon": "fa-instagram"},
        {"name": "Facebook", "url": "#", "icon": "fa-facebook"},
    ],
    "copyright_name": "Jane Doe",
    "design_credit_url": "http://html5up.net",
}


@app.route("/")
def home():
    """ホームページを表示する"""
    return render_template("index.html", data=SITE_DATA)


@app.route("/submit_form", methods=["POST"])
def submit_form():
    """フォームの送信を処理する"""
    # 本来はここでフォームデータを処理します（例：データベース保存、メール送信）
    # 今回は受け取ったデータをコンソールに出力するだけにします
    print("Form submitted:")
    for key, value in request.form.items():
        print(f"  {key}: {value}")
    # フォーム送信後のサンキューページや、元のページへのリダイレクトなどを返す
    return "<h1>Thank you for your message!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
