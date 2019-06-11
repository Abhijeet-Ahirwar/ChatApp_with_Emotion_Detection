# app.py

from flask import Flask, request, jsonify, render_template, redirect
import os
import pusher
from database import db_session
from models import User, Channel, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)

app = Flask(__name__)
pusher = pusher.Pusher(
	app_id=os.getenv('PUSHER_APP_ID'),
	key=os.getenv('PUSHER_KEY'),
	secret=os.getenv('PUSHER_SECRET'),
	cluster=os.getenv('PUSHER_CLUSTER'),
	ssl=True)
app.config['JWT_SECRET_KEY'] = '8818959301'  # Important
jwt = JWTManager(app)
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

@app.route('/')
def index():
    return jsonify("Pong!")

@app.route('/api/register', methods=["POST"])
def register():
	data = request.get_json()
	username = data.get("username")
	password = generate_password_hash(data.get("password"))
	try:
		new_user = User(username=username, password=password)
		db_session.add(new_user)
		db_session.commit()
	except:
		return jsonify({
                "status": "error",
                "message": "Could not add user"
            })
	return jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201


@app.route('/api/login', methods=["POST"])
def login():
	data = request.get_json()
	username = data.get("username")
	password = data.get("password")
	user = User.query.filter_by(username=username).first()

	if not user or not check_password_hash(user.password, password):
		return jsonify({
                "status": "failed",
                "message": "Failed getting user"
            }), 401

	access_token = create_access_token(identity=username) # Generate a token

	return jsonify({
		"status": "success",
    	"message": "login successful",
    	"data": {
    	"id": user.id,
    	"token": access_token,
    	"username": user.username
    	}
    	}), 200


# run Flask app
if __name__ == "__main__":
    app.run()