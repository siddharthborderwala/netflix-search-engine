from flask.app import Flask

app = Flask(__name__)


@app.get("/")
def root():
    return "Hello, World!"
