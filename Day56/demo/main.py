import os

from flask import Flask, render_template

app = Flask(__name__)

# サイトのコンテンツデータを一元管理
SITE_DATA = {
    "page_title": "My Personal Site",
    "name": "Your Name",
    "bio": "Web Developer & Designer",
    "profile_image": "images/avatar.jpg",  # static/images/profile.jpg を想定
    "skills": ["Python", "Flask", "HTML & CSS", "JavaScript"],
    "social_links": [
        {"name": "GitHub", "url": "#"},
        {"name": "LinkedIn", "url": "#"},
        {"name": "Twitter", "url": "#"},
    ],
}


@app.route("/")
def home():
    """ホームページをレンダリング"""
    return render_template("index.html", site=SITE_DATA)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
