from fastapi import FastAPI, Security
import toml
import publisher

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_message"]

app_config = get_app_config()

app = FastAPI(
    title=app_config["title"],
    description=app_config.get("description"),
    version= app_config.get("version")
)

@app.get('/')
def health():
    return({
        "status": "UP"
    })

@app.post("/send-request")
def send_request_to_queue(message: publisher.Message):
    publisher.send_request(addresses_id=message.addresses_id,
                           request=message.request,
                           sender_id=message.sender_id,
                           payload=message.model_dump())
