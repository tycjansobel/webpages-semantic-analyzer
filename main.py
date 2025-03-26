from dotenv import load_dotenv
load_dotenv(override=True)

import os
import api.endpoints as endpoints

from fastapi import FastAPI
from infrastructure.di.containers import Container
from fastapi.middleware.cors import CORSMiddleware

origins = os.getenv('CORS_ORIGINS', 'localhost:3000').split(';')

def app_factory() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["*"],
    )
    app.container = container
    app.include_router(endpoints.router)


    return app

app = app_factory()