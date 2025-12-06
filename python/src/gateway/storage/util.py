import pika
import json
import pika.spec

# f=uploaded file, fs=gridfs instance, channel=rabbitmq channel, access=claims containing username, exp, iat, admin
def upload(f, fs, channel, access):
    try:
        # put file into gridfs(mongodb), returns the file id if put is successful
        fid = fs.put(f)
    except Exception as err:
        return "internal server error", 500

    # if file upload is successful, send a message to the rabbitmq queue for the worker to process
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }
    
    try:
        # publish the message to the rabbitmq queue
        channel.basic_publish(
            exchange="",  # default exchange
            routing_key="video",  # queue name as the routing key for the default exchange
            body=json.dumps(message), # convert dict to JSON formatted string (opposite to json.loads)
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # make message persistent (since the pod for rabbitmq queue is a stateful pod 
            )                                                    # within the kubernetes cluster, so we need to make sure that when messages 
        )                                                        # are added to the queue, they are persisted if the pod restarts)
    except:
        # delete the file from gridfs if message publishing fails (if no message is published, the worker will not know that a new video has been uploaded), avoiding stale files
        fs.delete(fid)
        return "internal server error", 500
