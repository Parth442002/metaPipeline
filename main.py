from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import Response
import os
from connectors.celery import celery
from connectors.database import init_db
from dotenv import load_dotenv
import os

load_dotenv()
init_db()
# Local Imports
from routes.userAuthRoutes import router as userAuthRouter
from routes.extractAudioRoutes import router as audioRouter
from routes.watermarkRoutes import router as watermarkRouter

app = FastAPI()

# ? Auth Routes
app.include_router(userAuthRouter, prefix="/auth", tags=["auth"])
app.include_router(audioRouter, prefix="/audio", tags=["audio"])
app.include_router(watermarkRouter, prefix="/watermark", tags=["watermark"])
