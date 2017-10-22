from flask import Flask, request, Response
from password import passwd
import json
from flask.ext.sqlalchemy import SQLAlchemy
import itertools
from operator import itemgetter

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://familyadmin:' +passwd+'@famsource.cyszly6fwn7l.us-east-1.rds.amazonaws.com:3306/famsource'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/plans')
def plans():
    #get all plans
    if request.method == 'GET':
        plans = get_plans()
        return json.dumps(plans) 
    
@app.route('/services', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'GET':
        plans = db.engine.execute("SELECT service_name, service_max_capacity FROM services")
        res = []
        for row in plans:
            res.append({'service_name': row[0], 'service_max_capacity': row[1]})
        return json.dumps(res)
    if request.method =='POST':
        plan_name = request.json['plan_name']
        users = request.json['users']
        plan_capacity = request.json['plan_capacity']
        create_plan = db.engine.execute("INSERT INTO plans(plan_name, plan_capacity) VALUES (%s, %s)", plan_name, plan_capacity)
        get_last_insert_id = db.engine.execute("SELECT MAX(plan_id) FROM plans")
        last_insert_id = get_last_insert_id.fetchone()['MAX(plan_id)']
        services = request.json['services']
        
        for user in users:
            get_user_id = db.engine.execute("SELECT user_id FROM users where email=%s",user)
            user_id = get_user_id.fetchone()['user_id']
            try: 
                add_user_plans = db.engine.execute("INSERT INTO user_to_plan(user_to_plan_user_id, user_to_plan_plan_id) VALUES ("+ str(user_id)+ ","+ str(last_insert_id)+")")
            except Exception as e:
                print('\n\n\n\n\n\n\n\n')
                print(e, type(last_insert_id), type(user_id))
        for service in services:
            get_service_id = db.engine.execute("SELECT service_id FROM services WHERE service_name=%s",service)
            service_id = get_service_id.fetchone()[0]
            add_service_plans = db.engine.execute("INSERT INTO service_to_plan(service_to_plan_plan_id, service_to_plan_service_id) VALUES({},{})".format(last_insert_id, service_id))
        db.session.commit()
        return Response(status=200)

@app.route('/plans/<id>', methods=['GET', 'POST'])
def plan_details(id):
    if request.method=='GET':
        get_details = db.engine.execute("SELECT service_name, service_max_capacity, plan_name, plan_capacity FROM services NATURAL JOIN service_to_plan NATURAL JOIN plans WHERE service_to_plan_plan_id=%s", id)
        services = []
        plan_name =""
        plan_capacity =0
        for detail in get_details:
            plan_name=detail['plan_name']
            plan_capacity=detail['plan_capacity']
            services.append({'service_name':detail['service_name'],'service_max_capacity':detail['service_max_capacity']})
        get_users = db.engine.execute("SELECT first_name, review_value FROM users NATURAL JOIN user_to_plan NATURAL JOIN user_reviews WHERE user_to_plan_plan_id=%s", id)
        users = []        
        for user in get_users:
            users.append({'first_name': user['first_name'], 'review_value':user['review_value']})
        return json.dumps({'services':services, 'users':users, 'plan_capacity':plan_capacity, 'plan_name':plan_name})
    if request.method=='POST':
        user_id = request.json['user_id']
        update_user_subscription = db.engine.execute("INSERT INTO user_to_plan(user_to_plan_user_id, user_to_plan_plan_id) VALUES (%s,%s)", user_id, id)
        db.session.commit()
        return Response(status=200)

# @app.route('/<user_id>/plans')
# def get_all_plans(user_id):
#     if request.method=='GET':
#         get_user_plans = db.engine.execute("SELECT plan_name, plan_capacity, plan_id FROM plans NATURAL JOIN user_to_plan WHERE user_id=%s", user_id)
#         res = []
#         for plan in get_user_plans:
#             res.append({'plan_name': plan['plan_name'], 'plan_capacity' :plan['plan_capacity'], 'plan_id': plan['plan_id'], services:[]})
#         for result in res :
#             get_services=db.engine.execute("SELECT service_name, service_max_capacity FROM services NATURAL JOIN service_to_plan WHERE plan_id=%s", result['plan_id'])


def get_plans():
    get_plans = db.engine.execute("SELECT plan_name, plan_capacity, plan_id FROM plans WHERE plan_public=True")
    res = []
    for row in get_plans: 
        get_services = db.engine.execute("SELECT service_name FROM services NATURAL JOIN service_to_plan NATURAL JOIN plans WHERE plan_id = %s",row[2])
        res.append({'plan_name':row[0], 'plan_capacity':row[1], 'plan_id':row[2], 'services': []})
        for service in get_services:
            res[len(res)-1]['services'].append(service)
        get_user_count = db.engine.execute("SELECT count(*) FROM plans NATURAL JOIN user_to_plan WHERE plan_id=%s", row[2])
        res[len(res)-1]['user_count']=get_user_count.fetchall()[0]
    return res