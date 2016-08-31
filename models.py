#!/usr/bin/env python
import os
import sys
import ConfigParser
import json
from passlib.apps import custom_app_context as pwd_context
#pymongo
import pymongo
from pymongo import MongoClient
config = ConfigParser.ConfigParser()
config.read("config.cnf")


#mongodb
ip_address = config.get('mongodb', 'ip_address')
port = int(config.get('mongodb', 'port'))
mongo_url = config.get('mongodb', 'mongo_url')
database = config.get('mongodb', 'database')
users_collection = config.get('mongodb', 'users_collection')
post_collection = config.get('mongodb', 'post_collection')
comment_collection = config.get('mongodb', 'comment_collection')
mongo_user = config.get('mongodb', 'mongo_user')
mongo_pwd = config.get('mongodb', 'mongo_pwd')



class User():
    def __init__(self, *args, **kwargs):
        global users, password_hash
        try:
            client = MongoClient(mongo_url)
        except Exception as e:
            print("MongoDB connection establishment failed")
        try:
            db = client[database]
            db.authenticate(mongo_user, password=mongo_pwd)
        except Exception as e:  
            print("DB Instance connection failed")
        try:
            users = db[users_collection]
        except Exception as e:
            print("Unable to get collection handle")

    def insert_user(self, username, password):
        global users
        next_id = 1
        try:
          prev = users.find_one(sort=[("_id", -1)])
          next_id = prev["_id"] + 1
        except Exception as e:
          print("No collection exists at the moment to get the maximum _id value")

        user_data = {}
        user_data["_id"]  = next_id
        user_data['user_name'] = username
        user_data['password'] = password
        db_result = users.insert_one(user_data).inserted_id
        if(db_result):
          return db_result
        else:
          return False

    def get_user(self, username):
        global users
        db_result = users.find_one({"user_name": username})
        if db_result is not None:
          return db_result
        else:
          return False
    
    def get_user_by_id(self, id):
        global users
        db_result = users.find_one({"_id": id})
        if db_result is not None:
          return db_result
        else:
          return False

    def hash_password(self, password):
        global password_hash
        password_hash = pwd_context.encrypt(password)
        return password_hash

    def verify_password(self, username, password):
        db_result = users.find_one({"user_name": username})
        if db_result is not None:
                return pwd_context.verify(password, db_result['password'])
        return False

        
##########################################################
# Handling the Posts
##########################################################
class Blog():
    # __tablename__ = config.get('sqlite', 'post_table')
    # id = db.Column(db.Integer, primary_key=True)
    # created_at = db.Column(db.DateTime(),default=datetime.datetime.utcnow())
    # title = db.Column(db.String)
    # des = db.Column(db.String)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # comments = db.relationship('Comment', backref='title', lazy='dynamic')
    def __init__(self, *args, **kwargs):
        global posts, password_hash
        try:
            client = MongoClient(mongo_url)
        except Exception as e:
            print("MongoDB connection establishment failed")
        try:
            db = client[database]
            db.authenticate(mongo_user, password=mongo_pwd)
        except Exception as e:
            print("DB Instance connection failed")
        try:
            posts = db[post_collection]
        except Exception as e:
            print("Unable to get collection handle")

    def insert_post(self, title, body, user_id):
        global posts
        next_id = 1
        try:
          prev = posts.find_one(sort=[("_id", -1)])
          next_id = prev["_id"] + 1
        except Exception as e:
          print("No collection exists at the moment to get the maximum _id value")

        post_data = {}
        post_data["_id"]  = next_id
        post_data['title'] = title
        post_data['body'] = body
        post_data['user_id'] = user_id
        db_result = posts.insert_one(post_data).inserted_id
        if(db_result):
          return db_result
        else:
          return False

    def get_posts(self):
        global posts
        db_result = posts.find()
        if db_result is not None:
          return db_result
        else:
          return False

    def get_post_by_id(self, id):
        global posts
        db_result =  posts.find_one({"_id": id})
        if db_result is not None:
          return db_result
        else:
          return False

    def update_post(self, id, key, data):
        global posts
        status = posts.update_one({"_id": id}, {"$set": {key: data}}).acknowledged
        if status:
            return True
        else:
            return False
    
    def delete_post(self, id):
        global posts
        status = posts.delete_one({"_id" : id})
        if status:
            return True
        else:
            return False

# ##########################################################
# # Handling the Comments
# ##########################################################
class Comment():
    def __init__(self, *args, **kwargs):
        global comments
        try:
            client = MongoClient(mongo_url)
        except Exception as e:
            print("MongoDB connection establishment failed")
        try:
            db = client[database]
            db.authenticate(mongo_user, password=mongo_pwd)
        except Exception as e:
            print("DB Instance connection failed")
        try:
            comments = db[comment_collection]
        except Exception as e:
            print("Unable to get collection handle")
        
    def insert_comment(self, comment, user_id, post_id, parent_comment_id = 0):
        global comments
        next_id = 1
        try:
          prev = comments.find_one(sort=[("_id", -1)])
          next_id = prev["_id"] + 1
        except Exception as e:
          print("No collection exists at the moment to get the maximum _id value")

        comment_data = {}
        comment_data["_id"]  = next_id
        comment_data['comment'] = comment
        comment_data['post_id'] = post_id
        comment_data['user_id'] = user_id
        comment_data['parent_id'] = parent_comment_id
        db_result = comments.insert_one(comment_data).inserted_id
        if(db_result):
          return db_result
        else:
          return False

    def get_comment(self, id):
        global comments
        db_result = list(comments.find({"post_id":id}))
        if db_result is not None:
          return db_result
        else:
          return False

    def get_comment_by_id(self, id):
        global comments
        db_result = comments.find({"_id":id})
        if db_result is not None:
            return db_result
        else:
            return False

    def delete_comment(self, id):
        global comments
        db_result = comments.remove({'post_id':id})
        print db_result
        if db_result:
            return True
        else:
            return False

       

    
