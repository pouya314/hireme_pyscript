from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('hireme'))


@app.route('/hireme')
def hireme():
    return render_template('index.html')


@app.route('/wizard')
def wizard():
    return render_template('wizard.html', root_url=request.url_root)


@app.route('/up')
def up():
    return 'ok'


if __name__ == '__main__':
    app.run()
