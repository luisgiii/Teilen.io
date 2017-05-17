from flask import Flask
app = Flask(__name__)

@app.route("/")
def main_page():
    return "Welcome to Teilen.io!"

if __name__ == "__main__":
    app.run()
