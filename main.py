from flask import Flask,render_template,request, url_for, session, redirect, flash
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from konfig import Config
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
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
