from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from studywithroy import db
from werkzeug.security import generate_password_hash,check_password_hash
from studywithroy.models import User, BlogPost
from studywithroy.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from studywithroy.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, #form 자체가 email이 이미 있는지 없는지 확인할거임
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit() #db에 저장하기
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
        #indentation에 주목하기
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        #user = User.query.flter_by(email=form.email.data).first()
        #로그인 data체크하는 것은 꼭 알아야
        #이미 있는 것을 query하는 것임

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')
#아주 매력적인 form
            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user() #로그아웃시키기 -> flask_login에 있는 방법임
    return redirect(url_for('core.index')) #logout을 하면 home으로 보낸다


@users.route("/account", methods=['GET', 'POST'])
@login_required #로그인이 필요합니다
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic#지금 이 유저에게 저장하세요

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
#유저 네임 말할때 <>을 쓴다
def user_posts(username):
#이 템플릿에 들어왔을때, username을 pass in 한다
    page = request.args.get('page', 1, type=int)
    #
    user = User.query.filter_by(username=username).first_or_404() # <-있지 않으면, 404에러를 반환한다
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
        #                                author가 user인 것을 query한다. ORM인데, desc순으로 !

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
