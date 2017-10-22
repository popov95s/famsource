from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext import admin
from flask.ext.admin.contrib import sqla
from password import passwd

# Create application
app = Flask(__name__)


# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://familyadmin:' +passwd+'@famsource.cyszly6fwn7l.us-east-1.rds.amazonaws.com:3306/famsource'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
	return '<a href="/admin/">Click me to get to Admin!</a>'


# Create models
class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	email = db.Column(db.String(120), unique=True)

	# Required for administrative interface. For python 3 please use __str__ instead.
	def __unicode__(self):
		return self.email

class UserToPlan(db.Model):
	__tablename__ = 'user_to_plan'
	user_to_plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_to_plan_plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
	user_to_plan_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	def __unicode__(self):
		return self.user_to_plan_id

class Plan(db.Model):
	__tablename__='plans'
	plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	plan_capacity = db.Column(db.Integer)
	plan_name = db.Column(db.String(32))
	plan_public = db.Column(db.Boolean)
	def __unicode__(self):
		return self.plan_name

class Service(db.Model):
	__tablename__ = 'services'
	service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_name = db.Column(db.String(32))
	service_max_capacity = db.Column(db.Integer)
	service_min_capacity = db.Column(db.Integer)
	service_cost = db.Column(db.Float)

	def __unicode__(self):
		return self.service_name

class ServiceToPlan(db.Model):
	__tablename__ = 'service_to_plan'
	service_to_plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_to_plan_plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
	service_to_plan_service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
	def __unicode__(self):
		return (str(self.service_to_plan_plan_id) + " " + str(self.service_to_plan_service_id))

class UserReviews(db.Model):
	__tablename__ = 'user_reviews'
	review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	review_string = db.Column(db.String(512))
	review_value = db.Column(db.Integer)
	reviewed_by_user = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	# Required for administrative interface. For python 3 please use __str__ instead.
	def __unicode__(self):
		return self.review_id

class ServiceAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['service_id', 'service_name', 'service_max_capacity','service_min_capacity','service_cost']

class ServiceToPlanAdmin(sqla.ModelView):
   	column_display_pk = True
   	form_columns = ['service_to_plan_id', 'service_to_plan_plan_id', 'service_to_plan_service_id']

class UserAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['user_id', 'first_name', 'last_name','email']


class PlanAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['plan_id', 'plan_name','plan_capacity', 'plan_public' ]

class UserToPlanAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['user_to_plan_id', 'user_to_plan_user_id', 'user_to_plan_plan_id']

class UserReviewsAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['review_id','user_id','review_string','review_value','reviewed_by_user']


# Create admin
admin = admin.Admin(app, name='FamSource admin tool')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(PlanAdmin(Plan, db.session))
admin.add_view(UserToPlanAdmin(UserToPlan, db.session))
admin.add_view(ServiceAdmin(Service, db.session))
admin.add_view(ServiceToPlanAdmin(ServiceToPlan, db.session))
admin.add_view(UserReviewsAdmin(UserReviews, db.session))
if __name__ == '__main__':

	#db.drop_all()
	# Create DB
	db.create_all()

	# Start app
	app.run(debug=True)
