from pyscript import document


def get_root_url():
    return document.getElementById("root-url").innerHTML


# def get_fact_from_remote_api_server():
#     print('getting new cat fact from remote server')
#     response = requests.get('https://catfact.ninja/fact')
#     data = response.json()
#     return data['fact']
