import bcrypt
from app import app, db
from models import Users
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

# Define the admin interface.
admin = Admin(app, name = "Administrative Dashboard", template_mode = "bootstrap3")

# Define user login functionality.
login = LoginManager()
login.init_app(app)
login.login_view = "login"

# Admin model view definitions.
class UserModelView(ModelView):
	can_view_details = True
	column_labels = {"userID": "ID Number"}
	form_columns  = ("name", "username", "password", "role")
	form_choices  = {
		"role": [
			("Company", "Company"),
			("Admin", "Admin"),
		],
	}

	def create_model(self, form):
		user = Users()
		form.populate_obj(user)

		# Hash passwords before they go into storage.
		user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(4))

		user.userID = 10**8 + len(Users.getUsers())

		while len(Users.query.filter_by(userID=user.userID).all()) > 0:
			user.userID = 10**8 + len(Users.getUsers()) + 1

		self.session.add(user)
		self.session.commit()

		return True

	def after_model_change(self, form, model, is_created):
		user = Users()
		form.populate_obj(user)

		# Hash passwords before they go into storage.
		Users.query.filter_by(username=user.username).update({
			"password": bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(16))})

		self.session.commit()

		return True

admin.add_view(UserModelView(Users, db.session))

# handler to load user
@login.user_loader
def load_user(userID: int) -> Users:
	return Users.query.filter(Users.id == int(userID)).first()

