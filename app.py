# First we imported the Flask class. An instance of this class will be our WSGI application.
from flask import Flask

#
#
app = Flask(__name__)


# We then use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
