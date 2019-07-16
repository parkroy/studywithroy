import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

###설정

app.config['SECRET_KEY'] = 'mysecret'

###DB 셋업

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)


###Login 설정

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


###블루프린트 설정
from studywithroy.core.views import core
from studywithroy.users.views import users
from studywithroy.blog_posts.views import blog_posts
from studywithroy.error_pages.handlers import error_pages

app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
