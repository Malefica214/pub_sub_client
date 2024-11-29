from fastapi import FastAPI, Security, status
from fastapi.responses import JSONResponse
import toml
import publisher
import logger

log = logger.setup_logger()

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_message"]

def get_app_message():
    messages = toml.load("./pyproject.toml")
    return messages["message"]["it"]

app_config = get_app_config()
app_messages = get_app_message()

app = FastAPI(
    title=app_config["title"],
    description=app_config.get("description"),
    version= app_config.get("version")
)

log.info(f"Start {app_config["title"]} - Publisher")

@app.get('/', tags=["Publisher"])
def health():
    return({
        "status": "UP"
    })

@app.post("/send-request", tags=["Publisher"])
def send_request_to_queue(message: publisher.Message):
    try:
        log.debug(f"Avvio pubblicazione topic {message}")
        publisher.send_request(addresses_id=message.addresses_id,
                            request=message.request,
                            sender_id=message.sender_id,
                            payload=message.model_dump())
        log.inf(f"Pubblicazione avvenuta con successo")
        return JSONResponse(content={"message": app_messages.get("send_successfully")},
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error(f"Error on publish topic {e}")
        return JSONResponse(content={"message":app_messages.get("service_unavailable") },
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

