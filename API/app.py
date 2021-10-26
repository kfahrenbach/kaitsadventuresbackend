from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3
import os 
import base64

app = Flask(__name__)
cors = CORS(app)

# base directory. operating system - absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# instantiate
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(1000), unique=False)

    def __init__(self, name, email, content):
        self.name = name
        self.email = email
        self.content = content

class CommentSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'content')


# instantiate
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


# Endpoint to create a new comment
@app.route('/comment', methods=["POST"])
def add_comment():
    name = request.json['name']
    email = request.json['email']
    content = request.json['content']

    new_comment = Comment(name, email, content)
    db.session.add(new_comment)
    db.session.commit()

    comment = Comment.query.get(new_comment.id)

    return comment_schema.jsonify(comment)


# Endpoint to query all comments
@app.route('/comments', methods=["GET"])
def get_comments():
    all_comments = Comment.query.all()
    result = comments_schema.dump(all_comments)
    return jsonify(result)


# Endpoint for querying a comment
@app.route('/comment/<id>', methods=["GET"])
def get_comment(id):
    comment = Comment.query.get(id)
    return comment_schema.jsonify(comment)


# Endpoint for updating a comment
@app.route('/comment/<id>', methods=["PUT"])
def update_comment(id):
    comment = Comment.query.get(id)
    name = request.json['name']
    email = request.json['email']
    content = request.json['content']
    comment.name = name
    comment.email = email
    comment.content = content

    db.session.commit()
    return comment_schema.jsonify(comment)



# Endpoint for deleting a comment
@app.route('/comment/<id>', methods=["DELETE"])
def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()

    return comment_schema.jsonify(comment)



if __name__ == "__main__":
    app.run(debug=True)
