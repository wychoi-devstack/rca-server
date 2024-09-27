from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import CONF, configure
from api.v1 import api_router

PROJECT_NAME = "rca"

async def on_startup() -> None:
    configure(config_file_path='/etc/rca/rca.conf')

    # Set all CORS enabled origins
    if CONF.cors.allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in CONF.cors.allow_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

async def on_shutdown() -> None:
    pass

app = FastAPI(
    title=PROJECT_NAME,
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

app.include_router(api_router, prefix=constants.API_PREFIX)
