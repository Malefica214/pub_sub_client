# Pub/Sub Client Notification

This is a Pub/Sub project that establishes a connection to publish messages to a specific topic. The publisher is handled via an HTTP call using a FastAPI POST request.  

Later, a subscriber client can connect to a specific topic to view the queue of messages and process them.  

The idea is to have two users:  
- **User A** sends a friend request to **User B**.  
- **User B** receives the notification on their dashboard and can respond to it.  

## Authors

- **Francesca Buso** - Backend Software Engineer  
- **Francesco Pedini** - Full Stack Developer  

---

## Getting Started

You can clone this project and build your own Docker image or run the service locally  😊.

---

## Installing the MQTT Client - Mosquitto

1. Create subfolders for configurations, data, and logs in a directory:
    ```bash
    sudo mkdir ./srv/mosquitto/config ./srv/mosquitto/data ./srv/mosquitto/log -p
    ```
    *(It is recommended to stay in the same folder as the Docker Compose file, but this is optional.)*

2. Create the `mosquitto.conf` file to store all service configurations:
    ```bash
    sudo nano ./srv/mosquitto/config/mosquitto.conf
    ```

3. Add the following initial configurations in the editor:
    ```text
    persistence true
    persistence_location /mosquitto/data/
    log_dest file /mosquitto/log/mosquitto.log
    log_dest stdout
    listener 1883
    ```

4. Ensure Docker is installed on your machine.

5. Run the container using Docker Compose:
    ```bash
    sudo docker compose up -d
    ```
    To view logs, use:
    ```bash
    sudo docker compose logs -f
    ```
    *(The `-f` option keeps the log viewer active.)*

6. Once the container is running, configure the client credentials:
    - Access the container:
        ```bash
        docker exec -it mosquitto sh
        ```
    - Configure the credentials:
        ```bash
        mosquitto_passwd -c /mosquitto/config/mosquitto.passwd <USERNAME>
        ```
    - Exit the container with the `exit` command.

7. Update the `mosquitto.conf` file to include the credentials:
    - Open the file:
        ```bash
        sudo nano /srv/mosquitto/config/mosquitto.conf
        ```
    - Add the following lines:
        ```text
        password_file /mosquitto/config/mosquitto.passwd
        allow_anonymous false
        ```
    - Restart the container:
        ```bash
        docker container restart mosquitto
        ```

8. To allow WebSocket connections, add the following lines to the `mosquitto.conf` file:
    ```text
    listener 9001
    protocol websockets
    ```