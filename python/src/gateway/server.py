import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo

# custom modules
from auth import validate
from auth_svc import access
from storage import util
 
# creating a flask application instance
server = Flask(__name__)

server.config("MONGO_URI") = "mongodb://host.minikube.internal:27017/videos"

# initializing PyMongo with the Flask app instance
mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

# setting up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

# login route that communicates with auth service to log in a user and assign a token
@server.route("/login", methods=["POST"])
def login():
    # access.login returns a tuple, first item will go to token, second item will go to err(representing error)
    token, err = access.login(request)

    if not err:
        return token 
    else:
        return err 

# when a user uploads a video, they need to have a token which will be validated by the auth service
@server.route("/upload", methods=["POST"])
def upload():
    # access resolves to a JSON formatted string containing the payload (claims)
    access, err = validate.token(request)