from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('hireme'))


@app.route('/hireme')
def hireme():
    return render_template('index.html')


@app.route('/eligibility_and_application')
def eligibility_and_application():
    return render_template('eligibility_and_application.html')


@app.route('/up')
def up():
    return 'ok'


if __name__ == '__main__':
    app.run()
