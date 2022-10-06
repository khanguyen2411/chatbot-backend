from flask import Flask, redirect, url_for, request
# import chatbot
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_db

@app.route('/')
def hello():
    return "Hello world"


# @app.route('/message', methods=['GET'])
# def message():
#     return chatbot.answer(request.args.get("message"))


if __name__ == "__main__":
    app.run(debug=True)
