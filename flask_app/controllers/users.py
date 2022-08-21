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
   return render_template('registration.html')


@app.route('/register/user', methods=['POST'])
def register_user():
   if not User.validate_user(request.form):
      return redirect('/register')
   day= request.form['bithday']
   month = request.form['birthmonth']
   astrological_sign = get_astrological_sign(day, month)

   data = {
      'email': request.form['email'],
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'birthday': request.form['birthday'],
      'birthmonth': request.form['birthmonth'],
      'birthyear': request.form['birthyear'],
      'astrologicalSign_id': astrological_sign,
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
   return render_template('dashboard.html', users=users, user=user)


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/')

def get_astrological_sign(day,month):
   #ADDING ASTROLOGICAL SIGN TO USER
   day= request.form['bithday']
   month = request.form['birthmonth']
   if(month == 1):
      if(day < 20):
         astrological_sign = 1
      else:
         astrological_sign = 2
   elif(month == 2):
      if(day < 19):
         astrological_sign = 2
      else:
         astrological_sign = 3
   elif(month == 3):
      if(day < 21):
         astrological_sign = 3
      else:
         astrological_sign = 4
   elif(month == 4):
      if(day < 20):
         astrological_sign = 4
      else:
         astrological_sign = 5
   elif(month == 5):
      if(day < 21):
         astrological_sign = 5
      else:
         astrological_sign = 6
   elif(month == 6):
      if(day < 21):
         astrological_sign = 6
      else:
         astrological_sign = 7
   elif(month == 7):
      if(day < 23):
         astrological_sign = 7
      else:
         astrological_sign = 8
   elif(month == 8):
      if(day < 23):
         astrological_sign = 8
      else:
         astrological_sign = 9
   elif(month == 9):
      if(day < 23):
         astrological_sign = 9
      else:
         astrological_sign = 10
   elif(month == 10):
      if(day < 23):
         astrological_sign = 10
      else:
         astrological_sign = 11
   elif(month == 11):
      if(day < 22):
         astrological_sign = 11
      else:
         astrological_sign = 12
   elif(month == 12):
      if(day < 22):
         astrological_sign = 12
      else:
         astrological_sign = 1
   return astrological_sign