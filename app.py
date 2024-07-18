from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('hireme'))


@app.route('/hireme')
def hireme():
    return render_template('index.html')


@app.route('/up')
def up():
    return 'ok'


if __name__ == '__main__':
    app.run()
