from flask import Flask
from flask import request
import src.handlers.userHandler as userHandler

app = Flask(__name__)

@app.route('/')
def hello_geek():
    return 'Health Check'

@app.route('/user/register',methods = ['POST'])
def register_user():
    if request.method == 'POST':
        return userHandler.registerUser(request.json)
        


if __name__ == "__main__":
    app.run(debug=True)