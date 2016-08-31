#!/usr/bin/env python
import os
import sys
import ConfigParser
import datetime
from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from models import User, Blog, Comment

#Configuration
config = ConfigParser.ConfigParser()
config.read("config.cnf")
APP_SECRET = config.get('app', 'secret_key')


# initialization
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = APP_SECRET
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    auth = request.authorization
    user = User().get_user(auth.username)
    if (User().verify_password(auth.username,auth.password) == True):
        g.user = user
        return True
    return False


def arrangecomments(comments):
    tree = []
    for comment in comments:
        if(comment['parent_id'] == 0):
            tree.append(comment)
    

    def findreply(parent, comments, k = 0):
        if k == len(comments):
            return
        if comments[k] is not None:
            if(comments[k]['parent_id'] == parent['_id']):
                com = comments[k]
                findreply(com, comments)
                parent['reply'] = []
                parent['reply'].append(com)
            findreply(parent, comments, k+1)

    for parent in tree:
        findreply(parent, comments)
    

    return tree

@app.route('/', methods=['GET', 'POST'])
def posts():
    user = User()
    return jsonify({'status':'OK'});


##########################################################
# Register New User
##########################################################
@app.route('/api/add/users', methods=['POST'])
def new_user():
    user = User()
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if (user.get_user(username)):
        abort(400)    # existing user
    password = user.hash_password(password)
    response = user.insert_user(username, password)
    if(response):
        return (jsonify({'username': username}), 201,
                {'Location': url_for('get_user', id=response, _external=True)})
    else:
        return (jsonify({'Error' : 'Something went to wrong, Please Try again'}))


##########################################################
# Get User [Login User]
##########################################################
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User()
    user = user.get_user_by_id(id)
    if not user:
        abort(400)
    return jsonify({'username': user.user_name})



##########################################################
# Get All the Post
##########################################################
@app.route('/api/posts')
def show_posts():
    posts = Blog().get_posts()
    result = []
    if not posts:
        abort(400)    
    for post in posts:
        temp = {}
        temp['id'] = post["_id"]
        temp['title'] = post["title"]
        temp['body'] = post["body"]
        comments = Comment().get_comment(post["_id"])
        if comments is not None:
            tree = arrangecomments(comments)
            temp['comments'] = tree 
        result.append(temp)
    # result = [{col: getattr(d, col) for col in cols} for d in post]
    return jsonify({"Post":result})



##########################################################
# Add New Post
##########################################################
@app.route('/api/add/post', methods=['POST'])
@auth.login_required
def add_post():
    title = request.json.get('title')
    body = request.json.get('body')
    if title is None or body is None:
        abort(400)    # emety post data
    response = Blog().insert_post(title, body, g.user["_id"])
    if(response):
        return jsonify({'Response':'Success','Data' : 'Post Created'})
    else:
        return jsonify({'Response':'Failed','Data' : 'Post Not Created'})


####################################################################
# Update the post
####################################################################
@app.route('/api/update/posts/<int:id>', methods=['POST'])
@auth.login_required
def update_post(id):
    if id is None:
        abort(400);
    post = Blog().get_post_by_id(id)
    if not post:
        abort(400)
    if request.json.get('title') is not None:
        title = request.json.get('title')
        if ((Blog().update_post(id, "title" , title)) == False):
            return jsonify({'Response':'Failed','Data' : 'Post id-%d Not Updated' % id})
    if request.json.get('body') is not None:
        body = request.json.get('body');
        if ((Blog().update_post(id, "body" , body)) == False):
            return jsonify({'Response':'Failed','Data' : 'Post id-%d Not Updated' % id})
    return jsonify({'Response':'Success','Data' : 'Post id-%d Updated' % id})


####################################################################
# Delete the post
####################################################################
@app.route('/api/delete/posts/<int:id>', methods=['GET'])
@auth.login_required
def delete_post(id):
    if id is None:
        abort(400);
    post = Blog().get_post_by_id(id)
    if not post:
        abort(400)
    if(Blog().delete_post(id) == False):
        return jsonify({'Response':'Failed','Data' : 'Post id-%d Not Deleted' % id})
    response =  Comment().delete_comment(id)
    if(response):
        return jsonify({'Response':'Success','Data' : 'Post id-%d Deleted' % id})
    else:
        return jsonify({'Response':'Error','Data' : 'Post id-%d Deleted but comment of post id not deleted' % id})
    

##########################################################
# Add Comments to particular post
##########################################################
@app.route('/api/add/posts/<int:id>/comments', methods=['POST'])
@auth.login_required
def new_post_comment(id):
    post = Blog().get_post_by_id(id)
    comment = request.json.get('comment')
    if not post or comment is None:
        abort(400)    
    comment = Comment().insert_comment(comment, g.user["_id"], id)
    if(comment):
        return jsonify({'Response':'Success','Data' : 'User %d Post a comment On Post %d' % (g.user["_id"],id)})
    else:
        return jsonify({'Response':'Failed','Data' : 'Comment Not Posted'})



##########################################################
# Get the comments for particular post
##########################################################
@app.route('/api/comments/<int:id>')
def get_comment(id):
    comments = Comment().get_comment(id)
    if not comments:
        abort(400);
    tree = arrangecomments(comments)    
    return jsonify(comments=tree)


####################################################################
# Add Comments to particular Comment of the post [Threaded Comments]
####################################################################
@app.route('/api/add/posts/<int:postid>/comments/<int:commentid>', methods=['POST'])
@auth.login_required
def new_threaded_comment(postid,commentid):
    post = Blog().get_post_by_id(postid)
    comment = request.json.get('comment')
    if not Comment().get_comment_by_id(commentid):
        return jsonify({"Response" : 'False',"Data":'invalid Comment Id'})    
    if not post or comment is None:
        abort(400)    
    comment = Comment().insert_comment(comment, g.user["_id"], postid, commentid)
    if(comment):
        return jsonify({'Response':'Success','Data' : 'User %d Post a comment On Comment %d' % (g.user["_id"],commentid)})
    else:
        return jsonify({'Response':'Failed','Data' : 'Comment Not Posted'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
