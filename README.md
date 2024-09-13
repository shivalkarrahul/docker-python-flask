# docker-python-flask

This project demonstrates how to Dockerize a Flask application and set it up on an AWS EC2 instance. 

The goal is to first make you familiar with the manual setup of the application, providing a solid understanding of how each component works individually. Once you’re comfortable with the manual process, you’ll then learn how to streamline and simplify deployment using Docker. 

This README provides comprehensive instructions for both manual setup and Dockerized deployment. 

You will find detailed instructions for:

**Manual Setup**: Learn how to set up the Flask application manually without Docker, which provides insight into the configuration and challenges of a traditional deployment.

**Dockerized Setup**: Understand how to simplify and streamline deployment using Docker and Docker Compose, including detailed steps for running and managing containers.

## Overview

This project provides two approaches to setting up a Flask application:

**Manual Setup**: Run the application and its components manually on an AWS EC2 instance.

**Dockerized Setup**: Use Docker and Docker Compose on an AWS EC2 instance to automate the deployment process, ensuring a consistent and reproducible environment.


## Architectural Diagram

The architectural diagram below illustrates the components and their interactions in this project. 

![Architectural Diagram](images/architecture-diagram.png)

## Understand the Application

<details>
  <summary>Click to expand application details</summary>

### Flask Application

The Flask application is a Python web application built using the Flask framework. Flask is a lightweight web framework that is easy to set up and scale. It is used here to create a simple web service with a few endpoints.

**Files in the Flask Folder:**

- **`Dockerfile`**: This file contains the instructions to build a Docker image for the Flask application. It sets up the environment, installs dependencies, and defines how to run the Flask application.

- **`main.py`**: This is the main application file where the Flask web server is defined. It includes the routes and logic for handling HTTP requests.

- **`requirements.txt`**: This file lists the Python dependencies required for the Flask application. Docker uses this file to install the necessary packages inside the Docker container.

### Nginx Proxy

Nginx is used as a reverse proxy server to forward requests to the Flask application. It handles incoming HTTP requests and directs them to the Flask application container.

**Files in the Nginx Folder:**

- **`Dockerfile`**: This file contains the instructions to build a Docker image for the Nginx server. It sets up Nginx with the required configuration to serve as a reverse proxy.

- **`conf`**: This folder contains the Nginx configuration files. The primary configuration file, `default.conf`, sets up the proxy rules, such as forwarding requests to the Flask application and handling static files.

### Redis

In this setup, Redis is used solely to keep track of the application hit count. The Redis container is configured to work with the Flask application but does not have any associated files or directories in this project. 

</details>

## Manual Setup Instructions

<details>
  <summary>To understand how the application is configured and run without Docker, you can expand this section. If you're eager to jump directly to the Dockerized setup, you can skip this part.</summary>
  
<br>Before diving into the Dockerized setup of the Python Flask application, it’s valuable to understand the manual setup process. This section provides step-by-step instructions on how to set up the application from scratch without using Docker. By following these steps, you'll gain insights into the components involved and how they interact.

### Create an EC2 Instance on AWS

1. **Select Ubuntu Version:** 24.04 LTS
2. **Amazon Machine Image (AMI):** Ubuntu Server 24.04 LTS (HVM), SSD Volume Type (ami-0e86e20dae9224db8)
3. **Volume Size:** 30 GB (8 GB will also work)
4. **Instance Type:** t2.medium (t2.micro is also acceptable)
5. **Subnet:** Public
6. **SSH Key:** `workshop-docker-python-flask.pem` (Download the key on your machine)
7. **Security Group:** Allow SSH (port 22) and HTTP (port 80) for your IP

### Commands on Your Local Machine

1. **Set Permissions for Your SSH Key:**

    ```bash
    chmod 400 ~/Downloads/workshop-docker-python-flask.pem
    ```

2. **SSH into Your EC2 Instance:**

    ```bash
    ssh -i ~/Downloads/workshop-docker-python-flask.pem ubuntu@<EC2-Public-IP>
    ```
### Setup Application on the EC2 Instance

1. **Update and install necessary packages**
    ```bash
    sudo apt update
    ```

    ```bash
    sudo apt install python3-pip nginx redis-server
    ```

2. **Create directories and files for the Flask app**
    ```bash
    mkdir -p ~/my_flask_app
    ```
    
    ```bash
    cd ~/my_flask_app
    ```

    ```bash
    mkdir flask
    ```

    ```bash
    cd flask
    ```

    ```bash
    touch requirements.txt main.py
    ```

3. **Edit the `main.py` file**
    ```bash
    vim main.py
    ```

    Add the following code:
    ```python
    import redis
    from flask import Flask
    app = Flask(__name__)
    redis = redis.Redis(host='0.0.0.0', port=6379, db=0)

    @app.route('/')
    def hello_world():
        return 'This is a Python Flask Application with Redis accessed through Nginx'

    @app.route('/visitor')
    def visitor():
        redis.incr('visitor')
        visitor_num = redis.get('visitor').decode("utf-8")
        return "Visit Number = : %s" % (visitor_num)

    @app.route('/visitor/reset')
    def reset_visitor():
        redis.set('visitor', 0)
        visitor_num = redis.get('visitor').decode("utf-8")
        return "Visitor Count has been reset to %s" % (visitor_num)
    ```

4. **Create the `requirements.txt` file**
    ```bash
    vim requirements.txt
    ```

    Add the following:
    ```txt
    redis==3.4.1
    gunicorn>=20,<21
    Flask==2.0.3
    ```

5. **Install dependencies**

    ```bash
    pip3 install -r requirements.txt 
    ```
    You will face an issue here; ignore it and proceed. We will use Python Virtual Environment

    ```bash
    sudo apt install python3-venv
    ```

    ```bash
    python3 -m venv venv
    ```

    ```bash
    source venv/bin/activate
    ```

    ```bash
    pip install -r requirements.txt
    ```

6. **Run the app using Gunicorn**
    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 main:app
    ```

    You will face an issue here. We will fix it by adding the dependency in requirements.txt

7. **Freeze the dependencies (optional)**
    ```bash
    pip3 freeze
    ```

8. **Update the `requirements.txt` if necessary**

    update the requirements.txt

    ```bash
    vim requirements.txt
    ```
        
    ```txt
    redis==3.4.1
    gunicorn>=20,<21
    Flask==2.0.3
    Werkzeug==2.0.3
    ```

9. **Configure Nginx for proxying requests to the Flask app**
    ```bash
    sudo vim /etc/nginx/sites-available/my_flask_app
    ```

    Add the following configuration:
    ```nginx
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://127.0.0.1:8000;
        }

        location /hit {
            proxy_pass http://127.0.0.1:8000/visitor;
        }

        location /hit/reset {
            proxy_pass http://127.0.0.1:8000/visitor/reset;
        }
    }
    ```

10. **Link the Nginx configuration and restart Nginx**
    ```bash
    sudo ln -s /etc/nginx/sites-available/my_flask_app /etc/nginx/sites-enabled/
    ```

    ```bash
    sudo nginx -t
    ```

    ```bash
    sudo rm /etc/nginx/sites-enabled/default
    ```

    ```bash
    sudo systemctl restart nginx
    ```

11. **Access the application**
    - **Home Page:** `http://EC2-Public-IP:80/`
    - **Hit Endpoint:** `http://EC2-Public-IP:80/hit`
    - **Reset Endpoint:** `http://EC2-Public-IP:80/hit/reset`


<br> Hope you observed the complexity and issues we faced during the manual setup. Imagine replicating this process on multiple Development, QA, and Production machines. This is where Docker simplifies and streamlines the deployment process.

</details>


## Dockerized Setup Instructions

<details>
  <summary>To understand how to streamline the deployment of the application using Docker, you can expand this section.</summary>

### Create an EC2 Instance on AWS

1. **Select Ubuntu Version:** 24.04 LTS
2. **Amazon Machine Image (AMI):** Ubuntu Server 24.04 LTS (HVM), SSD Volume Type (ami-0e86e20dae9224db8)
3. **Volume Size:** 30 GB (8 GB will also work)
4. **Instance Type:** t2.medium (t2.micro is also acceptable)
5. **Subnet:** Public
6. **SSH Key:** `workshop-docker-python-flask.pem` (Download the key on your machine)
7. **Security Group:** Allow SSH (port 22) and HTTP (port 80) for your IP

### Commands on Your Local Machine

1. **Set Permissions for Your SSH Key:**

    ```bash
    chmod 400 ~/Downloads/workshop-docker-python-flask.pem
    ```

2. **SSH into Your EC2 Instance:**

    ```bash
    ssh -i ~/Downloads/workshop-docker-python-flask.pem ubuntu@<EC2-Public-IP>
    ```

### Setup Docker on the EC2 Instance

1. **Install Docker:**

    - **Update the package index and install prerequisites:**

        ```bash
        sudo apt-get update
        ```

        ```bash
        sudo apt-get install ca-certificates curl
        ```

    - **Add Docker’s GPG key:**

        ```bash
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        ```

    - **Add Docker’s repository:**

        ```bash
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ```

    - **Install Docker:**

        ```bash
        sudo apt-get update
        ```

        ```bash
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
        ```

    - **Verify Docker Installation:**

        ```bash
        sudo docker run hello-world
        ```

    - **Allow Non-Root User to Run Docker Commands:**

        ```bash
        sudo groupadd docker
        ```

        ```bash
        sudo usermod -aG docker $USER
        ```

        ```bash
        newgrp docker
        ```

2. **Clone the Project Repository:**

    ```bash
    cd /home/ubuntu/
    ```

    ```bash
    git clone https://github.com/shivalkarrahul/docker-python-flask.git
    ```

    ```bash
    cd docker-python-flask/
    ```

### Run the Application Manually

If you prefer to start each container manually, follow these steps:

1. **Start the Redis Container:**

    ```bash
    docker run -d --name redis redis:alpine
    ```

2. **Build and Start the Flask Application Container:**

    ```bash
    docker build -t flask flask/
    ```

    ```bash
    docker run -d --name app --link redis:redis -p 8000:8000 -v app:/app flask
    ```

3. **Build and Start the Nginx Proxy Container:**

    ```bash
    docker build -t nginx nginx/
    ```

    ```bash
    docker run -d --name proxy --link app:app -p 80:80 --restart always nginx
    ```

4. **Stop the Nginx Proxy, Flask and Redis Container:**

    ```bash
    docker stop proxy app redis
    ```
    

### Alternative: Using Docker Compose

For a simpler setup, you can use Docker Compose to manage all containers with a single command. Docker Compose can start the containers in the foreground or background, depending on your preference:


- **Start Containers in the Foreground:**

    ```bash
    docker compose up
    ```

    This command will start all containers and keep the terminal open with their logs.

- **Stop Containers running in the Foreground:**

    Press `Ctrl + C` in the terminal where `docker compose up` is running.

- **Start Containers in the Background:**

    If you want to run the containers in the background, add the `-d` flag:

    ```bash
    docker compose up -d
    ```

    This command will start the containers in detached mode, allowing you to continue using the terminal.

- **Stop and Remove Containers:**

    To stop and remove all containers created by Docker Compose, use:

    ```bash
    docker compose down
    ```

    This command will stop and clean up the containers, networks, and volumes defined in the `docker-compose.yml` file.


### Access the Application

- **Restart Containers:**

    As we have stopped the containers, start them again to access the application:

    ```bash
    docker compose up -d
    ```

- **Stop Containers:**

    ```bash
    docker compose down
    ```    

Once the application containers are running, you can access the application through your web browser:

- **Home Page:** [http://EC2-Public-IP:80/](http://EC2-Public-IP:80/)
- **Hit Endpoint:** [http://EC2-Public-IP:80/hit](http://EC2-Public-IP:80/hit)
- **Reset Endpoint:** [http://EC2-Public-IP:80/hit/reset](http://EC2-Public-IP:80/hit/reset)

Replace `EC2-Public-IP` with your EC2 instance's actual public IP address.

</details>

## Cleanup

To stop the application and clean up:

1. **Terminate the EC2 Instances:**

    Go to the AWS Management Console and terminate the EC2 instance to avoid incurring additional charges.


Feel free to reach out if you encounter any issues or have questions!    
    
