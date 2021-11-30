from waitress import serve

from server.app import app

if __name__ == "__main__":
    print("Server started at http://localhost:5000")
    serve(app, host="0.0.0.0", port=5000)
