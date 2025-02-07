from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("hireme"))


@app.route("/hireme")
def hireme():
    return render_template("index.html")


@app.route("/wizard")
def wizard():
    root_url = request.url_root
    if request.headers.get("X-Forwarded-Proto") == "https":
        root_url = root_url.replace("http://", "https://")
    return render_template("wizard.html", root_url=root_url)


@app.route("/up")
def up():
    return "ok"


if __name__ == "__main__":
    app.run()
