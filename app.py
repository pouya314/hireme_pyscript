from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hireme')
def hireme():
    return "Coming (back) soon!"


@app.route('/up')
def up():
    return 'ok'


if __name__ == '__main__':
    app.run()
