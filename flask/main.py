# Importing the Redis library to interact with a Redis database
import redis

# Importing the Flask library to create a web application
from flask import Flask

# Creating an instance of the Flask class for the web application
app = Flask(__name__)

# Connecting to the Redis server running on host 'redis' at port 6379 and using the default Redis database (db=0)
redis = redis.Redis(host='redis', port=6379, db=0)

# Defining a route for the root URL ('/') that returns a simple message when accessed
@app.route('/')
def hello_world():
     # The function returns a string that will be displayed on the homepage
     return 'This is a Python Flask Application with redis and accessed through Nginx'

# Defining a route for '/visitor' that increments and returns the visitor count
@app.route('/visitor')
def visitor():
     # Incrementing the 'visitor' key in the Redis database
     redis.incr('visitor')
     
     # Retrieving the current value of 'visitor' and decoding it from bytes to a UTF-8 string
     visitor_num = redis.get('visitor').decode("utf-8")
     
     # Returning the visit number as part of the response
     return "Visit Number = : %s" % (visitor_num)

# Defining a route for '/visitor/reset' to reset the visitor count to 0
@app.route('/visitor/reset')
def reset_visitor():
    # Setting the 'visitor' key in Redis to 0, effectively resetting the visitor count
    redis.set('visitor', 0)
    
    # Retrieving the updated value of 'visitor' and decoding it from bytes to a UTF-8 string
    visitor_num = redis.get('visitor').decode("utf-8") 
    
    # Returning a message indicating that the visitor count has been reset
    return "Visitor Count has been reset to %s" % (visitor_num)
