import requests
import json
from flask import Flask, request, render_template, redirect
from flask_login import login_user, LoginManager, \
        UserMixin, login_required, current_user, logout_user
from flask_cors import CORS
from app.auth import check_api_key, get_api_key, new_user
from config import ADMIN_ACCESS_TOKEN, URL_LIGHT_BACKEND 

app = Flask(__name__)
CORS(app)

app.config.update(
    SECRET_KEY = ADMIN_ACCESS_TOKEN,
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

user_now = ""

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username

    return user

## Basic wallet
@app.route('/')
def index():
    username = "Guest"

    if current_user is not None and current_user.is_authenticated:
        username =  current_user.id

    return render_template('index.html', url_light_backend = URL_LIGHT_BACKEND, \
            username = username)

## Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        data = request.form;

        # Login
        if check_api_key(data["name"], data["password"]) == True:
            user = User()
            user.id = data["name"]
            login_user(user, remember = True)

            return redirect("/")

## Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

## SignUp
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        data = request.form;

        # Local
        if new_user(data) == False:
            return {"status":"error","msg":"Account already exist."}


        # DID
        cred_headers = {"X-API-key": data["password"], "Content-Type":"application/json;"}
        cred = {"method": "light", "name": data["name"], "description": "Zhushan light eID", "pub_key":data["pub_key"]}

        # Request
        url_sned_token = URL_LIGHT_BACKEND + "/new_did"
        response = requests.post(url_sned_token, data = json.dumps(cred), headers = cred_headers)

        return redirect("/login")

## Payment
@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'GET':
        sender = ""

        if current_user is not None and current_user.is_authenticated:
            sender =  current_user.id

        receiver = request.args.get('receiver')
        
        return render_template('pay.html', url_light_backend = URL_LIGHT_BACKEND, \
                sender = sender, receiver_id = receiver)
    
    if request.method == 'POST':
        if current_user is None or not current_user.is_authenticated:
            return redirect("/login")

        data = request.form;

        # Get balance list
        url_balance = URL_LIGHT_BACKEND + "/get_balance?user="
        list_balance = requests.get(url_balance + str(data["sender"])).text.splitlines()

        if len(list_balance) < int(data["cost"]):
            return render_template('pay.html', msg="not enough")


        # Post header / credentials
        for index in range(int(data["cost"])):
            cred_headers = {"X-API-key": get_api_key(current_user.id), "Content-Type":"application/json;"}
            cred = {"sen": data["sender"], "rev": data["receiver"], "method": "2", "description": "Light token" ,"txn":list_balance[index]}

            # Request
            url_sned_token = URL_LIGHT_BACKEND + "/send_token"
            response = requests.post(url_sned_token, data = json.dumps(cred), headers = cred_headers)
        
        return render_template('pay.html')

## Wallet
@app.route('/wallet')
def walet():
    username = ""
    if current_user is not None and current_user.is_authenticated:
        username = current_user.id

    return render_template('wallet.html', url_light_backend = URL_LIGHT_BACKEND, \
            username = username)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8889, debug = True)
