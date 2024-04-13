from fastapi import FastAPI

from app.routers import admin_router
from app.routers import user_router

app = FastAPI(
    title="Сервис баннеров",
    version="1.0.0",
)

app.include_router(admin_router.router)
app.include_router(user_router.router)
