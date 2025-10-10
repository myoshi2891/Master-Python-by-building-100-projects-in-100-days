from flask import Flask
app = Flask(__name__)

@app.get("/")
def home(): return "Hello from pyenv venv!"

@app.get("/about")
def about(): return "This is the about page."

if __name__ == "__main__":
    app.run(debug=True)
