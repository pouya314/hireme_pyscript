import os
from flask import Flask, render_template, redirect, url_for, request, g
from flask_mail import Mail, Message
import git


def str_to_bool(s):
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot convert {s} to a boolean")


def get_git_version():
    """Get the current git commit hash using GitPython"""
    try:
        repo = git.Repo(search_parent_directories=True)
        commit = repo.head.commit
        return {
            'full_hash': commit.hexsha,
            'short_hash': commit.hexsha[:12],
            'version': commit.hexsha[:12]
        }
    except (git.InvalidGitRepositoryError, git.GitCommandError):
        return {
            'full_hash': 'unknown',
            'short_hash': 'unknown',
            'version': 'unknown'
        }


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = int(os.environ['MAIL_PORT'])
app.config['MAIL_USE_TLS'] = str_to_bool(os.environ['MAIL_USE_TLS'])
app.config['MAIL_USE_SSL'] = str_to_bool(os.environ['MAIL_USE_SSL'])
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
SENDER = os.environ['MAIL_SENDER']
RECEIVER = os.environ['MAIL_RECEIVER']
ENVIRONMENT_NAME = os.environ['ENVIRONMENT_NAME']

mail = Mail(app)


@app.before_request
def before_request():
    """Add git version to all templates"""
    g.git_version = get_git_version()


@app.route("/")
def index():
    return redirect(url_for("hireme"))


@app.route("/hireme")
def hireme():
    return render_template("index.html",
                           environment_name=ENVIRONMENT_NAME)


@app.route("/wizard")
def wizard():
    root_url = request.url_root
    if request.headers.get("X-Forwarded-Proto") == "https":
        root_url = root_url.replace("http://", "https://")
    return render_template("wizard.html",
                           root_url=root_url,
                           environment_name=ENVIRONMENT_NAME)


@app.route("/submit_application", methods=["POST"])
def submit_application():
    message = Message('New Job Opportunity Alert', sender=SENDER, recipients=[RECEIVER])

    data = request.get_json()
    questions = data.get('questions', [])
    transformed_questions = [f"{question['body']}\n{question['provided_answer']}" for question in questions]
    message_body = "\n\n".join(transformed_questions)

    message.body = message_body

    with app.app_context():
        mail.send(message)

    return "ok"


@app.route("/up")
def up():
    return "ok"


if __name__ == "__main__":
    app.run()
