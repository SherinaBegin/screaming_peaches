from crypt import methods
from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User
from flask_app.models.sign import Sign
from flask_app.models.comment import Comment

@app.route('/chatroom')
def chatroom():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(data)
    comments = Comment.get_all_comments()
    return render_template('chat_room.html', user=user, comments=comments)

@app.route('/chatroom/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Comment.validate_comment(request.form):
        return redirect('/chatroom')
    data = {
        'id': session['user_id']
    }
    comment_data = {
        'comment': request.form['comment'],
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    Comment.save(comment_data)
    return redirect('/chatroom')