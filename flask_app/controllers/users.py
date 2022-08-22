from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User
from flask_app.models.sign import Sign
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
   day= request.form['birthday']
   month = request.form['birthmonth']
   sign_id = get_astrological_sign(day, month)

   data = {
      'email': request.form['email'],
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'birthday': request.form['birthday'],
      'birthmonth': request.form['birthmonth'],
      'birthyear': request.form['birthyear'],
      'astrologicalSign_id': sign_id,
      'password': bcrypt.generate_password_hash(request.form['password'])
   }
   User.save(data)
   user = User.get_user_by_email(data)
   session['user_id'] = user.id
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
   sign_data = {
      'id': user.astrologicalSign_id
   }
   
   user = User.get_user_by_id(data)
   horoscope = Sign.get_by_id(sign_data)
   start_month = get_month(horoscope.start_month)
   end_month = get_month(horoscope.end_month)
   users = User.get_all_users()
   return render_template('dashboard.html', users=users, user=user, horoscope=horoscope, start_month=start_month, end_month=end_month)


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/')

def get_astrological_sign(day,month):
   print("you are in the get_astro_sign function")
   #ADDING ASTROLOGICAL SIGN TO USER
   if(int(month) == 1):
      if(int(day) < 20):
         return 1
      else:
         return 2
   elif(int(month) == 2):
      if(int(day) < 19):
         return 2
      else:
         return 3
   elif(int(month) == 3):
      if(int(day) < 21):
         return 3
      else:
         return 4
   elif(int(month) == 4):
      if(int(day) < 20):
         return 4
      else:
         return 5
   elif(int(month) == 5):
      if(int(day) < 21):
         return 5
      else:
         return 6
   elif(int(month) == 6):
      if(int(day) < 21):
         return 6
      else:
         return 7
   elif(int(month) == 7):
      if(int(day) < 23):
         return 7
      else:
         return 8
   elif(int(month) == 8):
      if(int(day) < 23):
         return 8
      else:
         return 9
   elif(int(month) == 9):
      if(int(day) < 23):
         return 9
      else:
         return 10
   elif(int(month) == 10):
      if(int(day) < 23):
         return 10
      else:
         return 11
   elif(int(month) == 11):
      if(int(day) < 22):
         return 11
      else:
         return 12
   elif(int(month) == 12):
      if(int(day) < 22):
         return 12
      else:
         return 1

def get_month(num):
   if num == 1:
      return "January"
   if num == 2:
      return "February"
   if num == 3:
      return "March"
   if num == 4:
      return "April"
   if num == 5:
      return "May"
   if num == 6:
      return "June"
   if num == 7:
      return "July"
   if num == 8:
      return "August"
   if num == 9:
      return "September"
   if num == 10:
      return "October"
   if num == 11:
      return "November"
   if num == 12:
      return "December"