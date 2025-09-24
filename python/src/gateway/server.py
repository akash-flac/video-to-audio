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

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    

