from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, cast

from flask import Flask

P = ParamSpec("P")
FuncType = Callable[P, str]

app = Flask(__name__)


@app.get("/")
def home() -> str:
    return (
        '<h1 style="text-align: center">Hello from pyenv venv!</h1>'
        "<p>This is paragraph 1.</p>"
        '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG0zbWI2d2JwaGwxeW14bXdtZ3VrcDg5M25heG85bnB6aTNydDFsOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o0vwzuFwCGAFO/giphy.gif" />'
    )

def html_wrapper(tag: str) -> Callable[[FuncType], FuncType]:
    def decorator(fn: FuncType) -> FuncType:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return f"<{tag}>{fn(*args, **kwargs)}</{tag}>"

        return cast(FuncType, wrapper)

    return decorator


make_bold = html_wrapper("b")
make_emphasis = html_wrapper("em")
make_underlined = html_wrapper("u")

@app.route("/about")
@make_bold
@make_emphasis
@make_underlined
def about() -> str:
    return "This is the about page."

@app.route("/greet/<path:name>/<int:number>")
def greet(name: str, number: int) -> str:
    return f"Hello {name}, you have accessed the greet route {number} times."

if __name__ == "__main__":
    app.run(debug=True)
