from api_endpoints import pdf_api, web_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.sessions import SessionMiddleware
import logging
import os

logging.basicConfig(filename='api.log', filemode='a', level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d- %(message)s')
app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the SessionMiddleware to enable session handling
# app.add_middleware(
#     SessionMiddleware, 
#     secret_key=os.environ.get("SESSION_SECRET", "dev-secret")
# )

app.include_router(pdf_api.router, tags=["PDF Question Answering"])
app.include_router(web_api.router, tags=["Web Data Question Answering"])