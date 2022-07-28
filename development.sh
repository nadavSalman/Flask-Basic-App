#!/usr/local/bin/bash

# If FLASK_APP is not set, the command will try to import “app” or “wsgi” (as a “.py” file, or package) 
# export FLASK_APP=app
# Alternative : $ python -m flask 

# To enable all development features, set the FLASK_ENV environment variable to development before calling flask run.
export FLASK_ENV=development
flask run



#  make the server publicly available from any ather client on your network.
# flask run --host=0.0.0.0