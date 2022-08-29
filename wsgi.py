# First we imported the Flask class. An instance of this class will be our WSGI application.
from flask import Flask, url_for, render_template, request
from markupsafe import escape
# from flask import url_for
# from flask import render_template
# from flask import request


# Based on the doc : https://flask.palletsprojects.com/en/2.2.x/quickstart/


app = Flask(__name__)


# We then use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def hello_world():
    return 'Hello World!'

# When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be escaped to protect from injection attacks.


@app.route('/a/<name>')
def end_point_a(name):
    return f"Hello, {escape(name)}!"


# Variable Rules
#  <converter:variable_name>.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


# To build a URL to a specific function, use the url_for() function.
# It accepts the name of the function as its first argument and any number of keyword arguments, each corresponding to a variable part of the URL rule.
# url_for([FUnction Name],[***URL Args ])
@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('profile', username='John Doe'))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


# HTTP Methods
# You can use the methods argument of the route() decorator to handle different HTTP methods.

'''
This example keeps all methods for the route within one function,
which can be useful if each part uses some common data.
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'POST to end point : /login'
    else:
        return 'GET to end point : /login'


# You can also separate views for different methods into different functions.
# Flask provides a shortcut for decorating such routes with get(), post(), etc. for each common HTTP method.
@app.get('/login2')
def login_get():
    return 'POST to end point : /login2'


'''
curl --location --request POST 'http://127.0.0.1:5000/login2' \
--header 'Content-Type: application/json'
'''


@app.post('/login2')
def login_post():
    return 'GET to end point : /login2'


# Static Files
with app.app_context(), app.test_request_context():
    url_for('static', filename='main.css')


# Rendering Templates
# Flask will look for templates in the templates folder
'''
Automatic escaping is enabled, so if name contains HTML it will be escaped automatically.
'''


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


# Accessing Request Data
@app.route('/login-1', methods=['POST', 'GET'])
def login1():
    error = None
    if request.method == 'POST':
        return valid_login(request.form['username'], request.form['password'])
    return None,404


def valid_login(user_name, password):
    if user_name == "babun" and password == "123":
        return {
            "massage": "your loged in ad system admin",
            "privilages": "write"
        }, 200
    else:
        return {
            "massage": "Forbidden access ",
            "privilages": "none"
        }, 403
        
        
# Test the endpoint /login-1 use :
    # curl --location --request POST 'http://127.0.0.1:5000/login-1' \
    # --header 'Content-Type: application/x-www-form-urlencoded' \
    # --data-urlencode 'username=babun' \
    # --data-urlencode 'password=123'


if __name__ == '__main__':
    app.run()
