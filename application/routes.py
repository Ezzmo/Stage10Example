from application import app, db, bcrypt
from flask import render_template, redirect, url_for, request
from application.forms import ChooseForm, RegistrationForm, LoginForm, UpdateAccountForm
from application.models import Userteams, Users, Players
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/board')
def home():
	teamData = Userteams.query.all()
	return render_template('home.html', title='Board', teams=teamData)

@app.route('/about')
def about():
    return render_template('about.html', title='about')
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hash_pw = bcrypt.generate_password_hash(form.password.data)
		user = Users(
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			email=form.email.data,
			password=hash_pw
			)

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('make'))

	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect('home')
	return render_template('login.html', title='Login', form=form)

@app.route('/make', methods=['GET', 'POST'])
@login_required
def make():
	form = ChooseForm()
	if form.validate_on_submit():
		teamData = Userteams(
			teamname = form.name.data,
			player1 = form.player1.data,
			player2 = form.player2.data,
			player3 = form.player3.data,
			player4 = form.player4.data,
			player5 = form.player5.data,
			user_id = current_user.id
		)
		db.session.add(teamData)
		db.session.commit()
		return redirect(url_for('home'))

	else:
		print(form.errors)
	return render_template('post.html', title='Post', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form=form)

@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
        user = current_user.id
        teams = Userteams.query.filter_by(user_id=user)
        for team in teamss:
                db.session.delete(team)
        account = Users.query.filter_by(id=user).first()
        logout_user()
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('register'))

@app.route("/board/clear", methods=["GET", "POST"])
@login_required
def board_delete():
        teams = Userteams.query.filter_by(user_id=user)
		for team in teams:
        	db.session.delete(team)
        	db.session.commit()
        return redirect(url_for('board'))
