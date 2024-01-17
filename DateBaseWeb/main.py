from fastapi import FastAPI

from Routes.admin_routes import admin_router
from Routes.worker_routes import worker_router

app = FastAPI()
app.include_router(worker_router)
app.include_router(admin_router)