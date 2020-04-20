import requests

def post_user(full_name, email, password):
    url = "http://localhost:8000/api/users/"
    data = {
        "full_name": full_name,
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Success!')
    else:
        print('Error!')

def send_email(email):
    url = "http://localhost:8000/api/password-reset/"
    data = {
        "email": email
    }
    response = requests.post(url, data=data)
    if response.status_code == 201:
        print('Success!')
    else:
        print('Error!')

def change_password(token, password):
    url = "http://localhost:8000/api/password-reset/" + token + "/"
    data = {
        "token": token,
        "password": password
    }
    response = requests.patch(url, data=data)
    if response.status_code == 201:
        print('Success!')
    else:
        print('Error!')

def get_users(request):
    url = "http://localhost:8000/api/users/"
    print(request.session)
    username = request.session['user_email']
    password = request.session['user_password']
    response = requests.get(url, auth=(username, password))
    users = response.json()
    users_list = {"users": users}
    return users_list
