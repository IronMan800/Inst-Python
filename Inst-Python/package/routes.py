import os

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from package import app, db, login_manager
from package.models import Users, Image


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)





@app.route('/all_users')
@login_required
def all_users():
    users = Users.query.all()
    return render_template('all_users.html', users=users)


@app.route('/reg', methods=['post', 'get'])
def reg():
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = generate_password_hash(request.form.get('password'))
        login = request.form.get('login')
        if login and password and username:
            users = Users.query.filter(Users.login == login).all()
            if users:
                flash('Данный пользователь зарегистрирован!', category='danger')
            else:
                user = Users(login=login, password=password, username=username, avatar='NULL')
                db.session.add(user)
                db.session.commit()
                flash('Вы успешно зарегистрированы!', category='success')
                return redirect(url_for('login'))
        else:
            flash('Заполните все поля!', category='danger')
    return render_template('reg.html')

@app.route('/')
@app.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        login_ = request.form.get('login')
        user = Users.query.filter(Users.login == login_).first()
        if user:
            if login_ and check_password_hash(user.password, request.form.get('password')):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Пароль не верный!', category='danger')
        else:
            flash('Пользователь не зарегистрирован', category='danger')
    return render_template('login.html')


@app.route('/image')
@login_required
def image():
    return render_template('user_image.html')


@app.route('/logout', methods=['post', 'get'])
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта!', 'success')
    return redirect(url_for('login'))


@app.route('/home', methods=['post', 'get'])
@login_required
def home():
    images = Image.query.order_by(desc(Image.Date)).all()
    return render_template('home.html', images=images)


@app.route('/edit_profile', methods=['post', 'get'])
@login_required
def edit_profile():
    if request.method == 'POST':
        if request.files['photo']:
            f = request.files['photo']
            f.filename = str(current_user.get_login()) + '.jpg'
            path = os.path.join('./package/static/images/avatar_user', f.filename)  # или path = os.path.join('./uploads', f.filename)
            f.save(path)
            user = Users.query.get(current_user.get_id())
            user.avatar = 'Yes'
            db.session.commit()
            flash('Фотография изменена!', 'success')
        if request.form.get('username'):
            username = request.form.get('username')
            user = Users.query.get(current_user.get_id())
            user.username = username
            db.session.commit()
            flash('Имя пользователя изменено!', 'success')
        return render_template('edit_profile.html')
    else:
        return render_template('edit_profile.html')


@app.route('/profile/<string:login>', methods=['post', 'get'])
@login_required
def profile(login):
    user = Users.query.filter(Users.login == login).first()
    images = Image.query.filter(Image.Login == login).order_by(desc(Image.Date)).all()
    if user:
        return render_template('profile.html', login=login, user=user, images=images)
    else:
        return 'Упс... Такого пользователя нет, но вы попробуйте еще раз, может найдете...'


@app.route('/add_image', methods=['post', 'get'])
@login_required
def add_image():
    if request.method == 'POST':
        f = request.files['Photo']
        NamePhoto = request.form.get('NamePhoto')
        Description = request.form.get('Description')
        Login = current_user.get_login()
        if NamePhoto and f:
            image = Image(Login=Login, NamePhoto=NamePhoto, Description=Description)
            db.session.add(image)
            db.session.commit()
            IdImage = Image.query.filter(Image.Login == Login).order_by(desc(Image.Date)).first()
            f.filename = str(IdImage.Id) + '.jpg'
            path = os.path.join('./package/static/images/Image_user', f.filename)
            f.save(path)
            flash('Вы успешно добавили фотографию!', category='success')
            return redirect(url_for('add_image'))
        else:
            flash('Заполните все поля!', category='danger')
    return render_template('add_image.html')