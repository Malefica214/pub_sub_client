from fastapi import FastAPI, Security, status
from fastapi.responses import JSONResponse
import toml
import publisher
import logger

log = logger.setup_logger()

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
    try:
        publisher.send_request(addresses_id=message.addresses_id,
                            request=message.request,
                            sender_id=message.sender_id,
                            payload=message.model_dump())
        return JSONResponse(content={"message": "Messaggio inviato con successo"},
                        status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error(f"Error on publish topic {e}")
        return JSONResponse(content={"message": "Servizio momentaneamente non disponibile"},
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

