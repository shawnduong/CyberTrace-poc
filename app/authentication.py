import time
import traceback

from app import *

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user

# Define the admin interface.
admin = Admin(app, name="Administrative Dashboard", template_mode="bootstrap3")

# Define user login functionality.
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

class UserModelView(ModelView):
	"""
	Admin model view for user type entries.
	"""

	can_view_details = True
	column_labels = {"acctType": "Account Type"}

	def create_model(self, form):
		"""
		Override default model creation behaviour to automatically hash the
		password as well after creation. Return True if successful.
		"""

		user = User()
		form.populate_obj(user)
		user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(4))
		db.session.add(user)
		db.session.commit()

	def get_edit_form(self):
		"""
		Override default model editing behaviour to not allow the admin to edit
		user passwords. Users must go through a password reset instead.
		"""

		form = super(UserModelView, self).get_edit_form()
		del form.password
		return form

admin.add_view(UserModelView(User, db.session))

@loginManager.user_loader
def load_user(id: int):
	"""
	Load a user using their id.
	"""

	return User.query.get(id)

@app.route("/login", methods=["POST"])
def login():
	"""
	Authenticate the user, or return an error message if unsuccessful. For
	security, a brief delay is added before the user authentication is checked
	in order to slow down enumeration and bruteforce/dictionary attacks.
	"""

	time.sleep(1)

	# User registration.
	if request.form["login-type"] == "signup":

		# Register the user.
		if User.register(request.form["username"], request.form["password"]):
			return render_template("index.html", pending=True)
		else:
			return render_template("index.html", rejected=True)

	# User login.
	elif request.form["login-type"] == "login":

		# Log the user in.
		user = User.login(request.form["username"], request.form["password"])

		# Failed login condition.
		if user == False:
			return render_template("index.html", failed=True)

		# Successful login, account type admin.
		elif user.acctType == 0:
			login_user(user)
			return redirect(url_for("admin.index"))

		# Successful login, account type non-admin.
		elif user.acctType == 1:
			# Stub.
			login_user(user)
			return redirect(url_for("stub"))

		# Successful login, account type pending.
		elif user.acctType == 2:
			return render_template("index.html", pending_approval=True)

	# Undefined behavior.
	else:
		return render_template("index.html")

