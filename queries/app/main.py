from fastapi import FastAPI
import uvicorn

from router import router

app = FastAPI()

app.include_router(router)

