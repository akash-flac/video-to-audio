# Distributed Video-to-Audio Microservices System
- Architected an **event-driven microservices application to convert large video files to MP3s**, utilizing RabbitMQ to decouple the API Gateway from heavy processing tasks and ensure non-blocking user interactions.
- Dockerized services (Auth, Gateway, Converter) using Kubernetes (Minikube), implementing **StatefulSets for queue**
persistence and **Ingress for traffic routing**.
- Implemented a hybrid database strategy, utilizing **MySQL for relational user data (Auth/JWT)** and **MongoDB GridFS
for sharded storage of large video/audio binary files**.
- Engineered a scalable consumer worker that processes conversion tasks **asynchronously** and triggers email alerts via
a dedicated **Notification service** upon completion.
> Tools and Libraries used: Python, Flask, Docker, Kubernetes, RabbitMQ, MongoDB, MySQL, Minikube
## Architecture:
<img width="2816" height="1536" alt="Gemini_Generated_Image_w8as6bw8as6bw8as" src="https://github.com/user-attachments/assets/3467eea5-9c96-46a8-9df9-5524645988ff" />

## Few Snapshots:
K9s is a terminal-based UI used to manage Kubernetes clusters. Here is a snapshot depicting auth, converter, gateway and rabbitmq pods in a running state:
<img width="1599" height="693" alt="Pasted image 20251208160514" src="https://github.com/user-attachments/assets/01091de1-511d-461e-945b-66aa2541e3bd" />

In order to interact with the system, a simple cURL request is required. Here is a snapshot of a cURL request to obtain a JWT token, which will then be used to upload a video: 
<img width="1919" height="977" alt="Pasted image 20251208191833" src="https://github.com/user-attachments/assets/57424778-0b27-499d-a9fc-dadcf77325aa" />

Once the conversion is done via the converter service, the mp3 is uploaded to local mongodb cluster, wherein `mongofiles` command-line utility can be used to download the mp3 to the local disk. Here is snapshot of the command usage in a git bash terminal:
<img width="743" height="438" alt="Pasted image 20251208194757" src="https://github.com/user-attachments/assets/93374d1b-ee89-4575-b7cb-f377ed73c192" />


