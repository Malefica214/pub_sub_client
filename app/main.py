from fastapi import FastAPI, Security
import toml
import messages

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

@app.post('/send-message')
def send_message(new_message: messages.Message):
    messages.publish_message(message=new_message)
    