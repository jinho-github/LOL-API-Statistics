from flask import Flask,render_template,request, url_for, session, redirect, flash
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import requests
import json
from konfig import Config
from urllib import parse
cc = Config("./conf.ini")

api_conf = cc.get_map("api")
app_conf = cc.get_map("app")
db_conf = cc.get_map("db")
app = Flask(__name__)
#DB와 비밀번호는 환경변수에서 가져온다.
app.config['SECRET_KEY'] = app_conf['SECRET_KEY']
app.config['MONGO_URI'] = db_conf['MONGO_URI']
apikey = api_conf['LOL_API_KEY']

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')
#에러페이지 404, 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login')
def login():
    # 카카오 로그인
    return render_template('login.html')


@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    resToken = getAccessToken("0341add84c6502731953a8e222053bc9",str(code))  # 발급받은 api key
    access_token = resToken.get("access_token") #유저정보를 받을 권한이 있는 토큰
    
    #access tokent 기반으로 유저 정보 요청
    profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
        )
    data = profile_request.json()
    print(data)
    
    # db에 등록된 email인지 체크
    # myuser = mongo.db.user_Info
    # existing_user = myuser.find_one({'email' : request.form['register_email']})
    # if existing_user is None:
    #     hashpass = bcrypt.generate_password_hash(request.form['register_pw2'])
    #     myuser.insert({'email' : request.form['register_email'], 'password' : hashpass})
    #     return redirect(url_for('home'))
    # # 있으면 루트 home.html로 redirect
    # else:
    #     print(str(code))
    #     print(str(resToken))
    return "test"
    

def getAccessToken(clientId, code) :  # 세션 코드값 이용, ACESS TOKEN / REFRESH TOKEN을 발급
    myurl = parse.quote("http://127.0.0.1:5000/") # 토큰 돌려받을 주소 (서버주소)
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + clientId
    payload += f"&redirect_uri={myurl}oauth&code=" + code
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
    }
    reponse = requests.request("POST",url,data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
