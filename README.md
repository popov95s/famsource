# famsource


To set up Flask app : 

1. Create virtual environment 
<code>virtualenv env</code>
2. Activate virtual environment
On Unix : 
<code>source env/bin/activate</code>
On Windows :
<code>env\Scripts\Activate</code>
3. Install requirements 
<code>pip install -r flask/requirements.txt</code>
4. Configure app
On Unix : 
<code>export FLASK_APP=app.py </code>
On Windows: 
<code>SET FLASK_APP=app.py</code>
5. Serve app
flask run --port=5001 --host=0.0.0.0


To set up DB Admin Tool: 
1. Install requirements 
<code>pip install -r database_utility/requirements.txt</code>

2. Add password.py file containing the password to DB in the form : 
passwd= DB_PASS

3. Serve app
python database_utility/admin.py
