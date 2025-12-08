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

server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

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
    if err:
        return err
    access = json.loads(access)

    # access is True if the user is an admin(admin attribute is True in the token payload), False otherwise
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly one file allowed", 400

        for _, f in request.files.items():
            # f=uploaded file, fs=gridfs instance, channel=rabbitmq channel, access=claims containing username, exp, iat, admin
            err = util.upload(f, fs, channel, access)

            if err:
                return err

        return "success", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
