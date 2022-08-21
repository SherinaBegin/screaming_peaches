from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User
from flask_app.models.sign import Sign


@app.route('/signs')
def all_signs():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(data)
    signs = Sign.get_all_signs()
    return render_template('astrological_signs.html', user=user, signs=signs)

@app.route('/signs/<int:sign_id>')
def view_sign(sign_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    sign_data = {
        'id': sign_id
    }
    user = User.get_user_by_id(data)
    sign = Sign.get_by_id(sign_data)
    return render_template('sign_view.html', user=user, sign=sign)
