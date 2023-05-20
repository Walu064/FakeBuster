# Libraries
import uvicorn

# Modules
from api.api import init_api
from api.conf.config import SERVER_HOST, SERVER_PORT


def run(host: str = SERVER_HOST, port: int = SERVER_PORT):
    api = init_api()
    uvicorn.run(api, host=host, port=port)


if __name__ == '__main__':
    run()
