# First we imported the Flask class. An instance of this class will be our WSGI application.
from flask import Flask, url_for, render_template, request ,abort, redirect
from markupsafe import escape
import random
import pycountry
from flask import after_this_request

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



#Cookies
'''

If you want to use sessions, do not use the cookies directly but instead use the Sessions in Flask that add some security on top of cookies for you.


Question :
 what is cookies : 
Answear :
 Cookies are key/value pairs used by websites to store state information on the browser.
 Say you have a website (example.com), when the browser requests a webpage the website can send cookies to store information on the browser

 Browser request example:

GET /index.html HTTP/1.1
Host: www.example.com
Example answer from the server:

HTTP/1.1 200 OK
Content-type: text/html
Set-Cookie: foo=10
Set-Cookie: bar=20; Expires=Fri, 30 Sep 2011 11:48:00 GMT
... rest  of the response
Here two cookies foo=10 and bar=20 are stored on the browser. The second one will expire on 30 September. In each subsequent request the browser will send the cookies back to the server.

GET /spec.html HTTP/1.1
Host: www.example.com
Cookie: foo=10; bar=20
Accept: */*


SESSIONS: Server side cookies
Server side cookies are known as "sessions". The website in this case stores a single cookie on the browser containing a unique Session Identifier. Status information (foo=10 and bar=20 above) are stored on the server and the Session Identifier is used to match the request with the data stored on the server.
'''
# Eaxmple :

languages = [country.name for country in pycountry.countries]
@app.before_request
def detect_user_language():
    language = request.cookies.get('country')
    if language is None:
        language_random_index = random.randint(0,len(languages) - 1)

        @after_this_request
        def remember_language(response):
            response.set_cookie('country', languages[language_random_index])
            return response

@app.route('/my-cookies', methods=['GET'])
def coocies_end_point():
    country = request.cookies.get('country')
    return {
            "massage": f"testing cookies {country}",
        }, 200



# Redirects and Errors
@app.route('/kuku1')
def index():
    #   abort(401)
    return redirect(url_for('coocies_end_point'))

if __name__ == '__main__':
    app.run()
