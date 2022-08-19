from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def landing():
   return render_template('login.html')


@app.route('/register')
def register():
   return render_template('register.html')


@app.route('/register/user', methods=['POST'])
def register_user():
   if not User.validate_user(request.form):
      return redirect('/register')
   data = {
      'email': request.form['email'],
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'password': bcrypt.generate_password_hash(request.form['password'])
   }
   id = User.save(data)
   session['user_id'] = id
   return redirect('/dashboard')


@app.route('/login/user', methods=['POST'])
def login_user():
   user = User.get_user_by_email(request.form)
   if not user:
      flash('Invalid Email')
      return redirect('/')
   if not bcrypt.check_password_hash(user.password, request.form['password']):
      flash('Invalid Password')
      return redirect('/')
   session['user_id'] = user.id
   return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
   if 'user_id' not in session:
      return redirect('/logout')
   data = {
      'id': session['user_id']
   }
   user = User.get_user_by_id(data)
   users = User.get_all_users()
   projects = Project.get_all_projects()
   return render_template('dashboard.html', users=users, user=user, projects=projects)


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/')
