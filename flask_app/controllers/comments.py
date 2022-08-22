from crypt import methods
from weakref import ref
from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User
from flask_app.models.sign import Sign
from flask_app.models.comment import Comment

@app.route('/chatroom/<int:sign_id>')
def chatroom(sign_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    sign_data = {
        'id': sign_id
    }
    user = User.get_user_by_id(data)
    users = User.get_all_users()
    horoscope = Sign.get_by_id(sign_data)
    comments = Comment.get_comments_by_sign(sign_data)
    return render_template('chat_room.html', user=user, users = users, comments=comments, horoscope = horoscope)

@app.route('/chatroom/add_comment/<int:sign_id>', methods=['POST'])
def add_comment(sign_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Comment.validate_comment(request.form):
        return redirect(f'/chatroom/{sign_id}')
    Comment.save(request.form)
    return redirect(f'/chatroom/{sign_id}')

@app.route('/view/comment/<int:comment_id>')
def view_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': comment_id
    }
    user_data = {
        'id': session['user_id']
    }
    comment = Comment.get_comment_by_id(data)
    return render_template('view_comment.html', comment = comment, user = User.get_user_by_id(user_data), users = User.get_all_users())

@app.route('/edit/comment/<int:comment_id>')
def edit_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': comment_id
    }
    user_data = {
        'id': session['user_id']
    }
    comment = Comment.get_comment_by_id(data)
    return render_template('edit_comment.html', comment = comment, users = User.get_all_users())

@app.route('/update/comment/<int:comment_id>', methods=['POST'])
def update_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Comment.validate_comment(request.form):
        return redirect(f'edit/comment/{comment_id}')
    Comment.update(request.form)
    return redirect(f'/view/comment/{comment_id}')

@app.route('/delete/comment/<int:comment_id>')
def delete_project(comment_id):
    data = {
        'id': comment_id
    }
    Comment.delete_comment(data)
    return redirect('/dashboard')
