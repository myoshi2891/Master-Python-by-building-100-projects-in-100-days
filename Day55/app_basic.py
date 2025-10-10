from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return (
        '<h1 style="text-align: center">Hello from pyenv venv!</h1>'
        "<p>This is paragraph 1.</p>"
        '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG0zbWI2d2JwaGwxeW14bXdtZ3VrcDg5M25heG85bnB6aTNydDFsOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o0vwzuFwCGAFO/giphy.gif" />'
    )

def make_bold(fn):
    def wrapper(*args, **kwargs):
        return f"<b>{fn(*args, **kwargs)}</b>"
    return wrapper

def make_emphasis(fn):
    def wrapper(*args, **kwargs):
        return f"<em>{fn(*args, **kwargs)}</em>"
    return wrapper

def make_underlined(fn):
    def wrapper(*args, **kwargs):
        return f"<u>{fn(*args, **kwargs)}</u>"
    return wrapper

@app.route("/about")
@make_bold
@make_emphasis
@make_underlined
def about():
    return "This is the about page."

@app.route("/greet/<path:name>/<int:number>")
def greet(name, number):
    return f"Hello {name}, you have accessed the greet route {number} times."

if __name__ == "__main__":
    app.run(debug=True)
