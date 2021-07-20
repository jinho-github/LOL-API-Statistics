from flask import Flask, current_app
import conf
from views.auth import auth
from views.error import err
from views.home import home

def create_app():
    app = Flask(__name__)
    #DB와 비밀번호는 환경변수에서 가져온다.
    with app.app_context():
    # within this block, current_app points to app.
        print(current_app.name)

    app.config['SECRET_KEY'] = conf.SECRET_KEY
    app.config['MONGO_URI'] = conf.MONGO_URI
    app.config['LOL_API_KEY'] = conf.LOL_API_KEY
    	
    app.register_blueprint(err)
    app.register_blueprint(auth)
    app.register_blueprint(home)

    return app

    


