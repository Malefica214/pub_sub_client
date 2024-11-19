from fastapi import FastAPI, Security
import toml

def get_app_config():
    config = toml.load("./pyproject.toml")
    return config["tool"]["bean_notification"]

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