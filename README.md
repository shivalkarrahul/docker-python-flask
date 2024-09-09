# docker-python-flask

Dockerize Flask Python Application

## Setup Instructions

### Create an EC2 Instance

1. **Ubuntu Version:** 22
2. **AMI:** ami-0e86e20dae9224db8
3. **Volume Size:** 30 GBs
4. **Instance Type:** t2.medium
5. **Subnet:** Public
6. **SSH Key:** `workshop-docker-python-flask.pem`
7. **Security Group:** Allow SSH(22) and HTTP(80) for your IP

### Commands on Your Local Machine

1. Set the correct permissions for your SSH key:

    ```bash
    chmod 400 ~/Downloads/workshop-docker-python-flask.pem
    ```

2. SSH into the EC2 instance:

    ```bash
    ssh -i ~/Downloads/workshop-docker-python-flask.pem ubuntu@ec2-184-72-166-229.compute-1.amazonaws.com
    ```

### Commands on the EC2 Instance

1. **Install Docker:**

    - Add Docker's official GPG key:

        ```bash
        sudo apt-get update
        sudo apt-get install ca-certificates curl
        sudo install -m 0755 -d /etc/apt/keyrings
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        sudo chmod a+r /etc/apt/keyrings/docker.asc
        ```

    - Add the repository to Apt sources:

        ```bash
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
          $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        ```

    - Install the latest version of Docker:

        ```bash
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```

    - Verify the installation:

        ```bash
        sudo docker run hello-world
        ```

    - Manage Docker as a non-root user:

        - Create the Docker group:

            ```bash
            sudo groupadd docker
            ```

        - Add your user to the Docker group:

            ```bash
            sudo usermod -aG docker $USER
            ```

        - Activate the changes to groups:

            ```bash
            newgrp docker
            ```

        - Verify that you can run Docker commands without `sudo`:

            ```bash
            docker run hello-world
            ```

2. **Clone the Repository and Run the Application:**

    ```bash
    cd /home/ubuntu/
    git clone https://github.com/shivalkarrahul/docker-python-flask.git
    cd docker-python-flask/
    docker compose up
    ```

### Access the Application

You can access the application at the following URLs:

- [http://EC2-Public-IP:80/](http://EC2-Public-IP:80/)
- [http://EC2-Public-IP:80/hit](http://EC2-Public-IP:80/hit)
- [http://EC2-Public-IP:80/hit/reset](http://EC2-Public-IP:80/hit/reset)

### Cleanup

To stop the application and clean up:

1. Press `Ctrl + C` in the terminal where `docker compose up` is running.
2. Terminate the EC2 instance.
    
