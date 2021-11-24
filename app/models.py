import bcrypt
from app import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String , unique = False, nullable = False)
	username = db.Column(db.String , unique = True , nullable = False)
	password = db.Column(db.String , unique = False, nullable = False)
	role = db.Column(db.String , unique = False, nullable = False)
	userID = db.Column(db.Integer, unique = True , nullable = False)

	# logs user in
	def login(username, password):
		return user if (
				(user := Users.query.filter_by(username=username).first()) != None 
				and bcrypt.checkpw(password.encode(), user.password)) else False

				
