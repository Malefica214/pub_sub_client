# Pub/Sub Client Notification
This is a pub/sub project that can open connection for publish a message in a specific topic, the publisher in handle by an HTTP call with FastApi POST request.
In a second moment a subscriber client can enter in a specific topic for view the queue message and precess them.

The idea is that you have two users, one of this send a friend request to other, this one receive the notifications in yur dashboard and can respond.

Authors:

**Francesca Buso** - Back end software engineer

**Francesco Pedini** - Full stack developer


## Getting started

You can clone this project and build your own docker image or run the service local.

## Install MQTT client - Mosquitto

1. In a folder create subfolder for configurations, data and logs:
    ```
    sudo mkdir ./srv/mosquitto/config ./srv/mosquitto/data ./srv/mosquitto/log -p
    ```
    I prefer to stay in the same folder of docker compose, but it's individual!

2. Create the `mosquitto.conf` file, where we put all service configuration 
    ```
    sudo nano ./srv/mosquitto/config/mosquitto.conf
    ```
3. In the editor put this initial configurations:
    ```
    persistence true
    persistence_location /mosquitto/data/
    log_dest file /mosquitto/log/mosquitto.log
    log_dest stdout
    listener 1883
    ```
4. Be sure to have docker installed on the pc
5. Run container with compose file: `sudo docker compose up -d`, then you can view the logs `sudo docker compose logs -f`, the option `-f` is for stay watching logs
6. When container run you can configure the client credentials:
    - Enter in container with active command line
        ```
        docker exec -it mosquitto sh
        ```
    - Configure credentials:
        ```
        mosquitto_passwd -c /mosquitto/config/mosquitto.passwd NOME_UTENTE
        ```
    - When all ok you can exit from container with `exit` command
7. Configure credential in the `mosquitto.conf` file:
    - `sudo nano /srv/mosquitto/config/mosquitto.conf`
    - Put new configuration lines:
        ```
        password_file /mosquitto/config/mosquitto.passwd
        allow_anonymous false
        ```
    - Restart container: `docker container restart mosquitto`
8. For allow the websocket port you must insert another configuration lins for open port into client container, you can edit another one time the `mosquitto.conf` file, and add this configuration:
    ```
    listener 9001
    protocol websockets
    ```