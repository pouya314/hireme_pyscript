import requests
from pyscript import document


def get_root_url():
    return document.getElementById("root-url").innerHTML


def get_data(filename):
    return requests.get(f"{get_root_url()}static/data/{filename}").json()
