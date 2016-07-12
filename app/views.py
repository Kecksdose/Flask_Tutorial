from flask import render_template, flash, redirect
from app import app, db
from .forms import UsernamePasswordForm
from .models import User

@app.route('/')
@app.route('/index/')
def index():
    user = {'nickname': 'Purzelin'}
    posts = [
        {
            'author': {'nickname': 'Timon'},
            'body': 'Alles Gute, Jana!'
        },
    ]
    return render_template('index.html',
        title='Home',
        user=user,
        posts=posts)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect('/index/')
    return render_template('register.html',
        title='Registrierung',
        form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first_or_404()
        if user.is_correct_password(form.password.data):
            flash('Du bist drin! Das war ja einfach...')
        else:
            flash('Da ist wohl was schiefgelaufen!')
        return redirect('/index/')
    return render_template('login.html',
        title='Anmeldung',
        form=form)
