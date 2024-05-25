import os.path

import coloredlogs
import uvicorn
from fastapi import FastAPI

from config import Config
from utils import ConfigProvider, PrettyJSONResponse

coloredlogs.install(level='INFO')
app = FastAPI()
provider = ConfigProvider()


@app.get("/{json_path}/{user_id}", response_class=PrettyJSONResponse)
def original(json_path: str, user_id: str):
    return provider.create_original(json_path, user_id)


@app.get("/{json_path}/{user_id}/{template}", response_class=PrettyJSONResponse)
def template(json_path: str, user_id: str, template: str):
    return provider.create_template(json_path, user_id, template)


if __name__ == "__main__":
    # to init app
    if Config.SSL_KEY_FILE and Config.SSL_CERT_FILE and \
            os.path.exists(Config.SSL_KEY_FILE) and os.path.exists(Config.SSL_CERT_FILE):
        uvicorn.run(
            'main:app', host='0.0.0.0', port=Config.PORT,
            ssl_keyfile=Config.SSL_KEY_FILE,
            ssl_certfile=Config.SSL_CERT_FILE)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=Config.PORT)
