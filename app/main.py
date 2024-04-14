from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.db.database import engine
from app.models.tables import Base
from app.routers import admin_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Сервис баннеров",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=400, detail="Некорректные данные")


app.include_router(admin_router.router)
app.include_router(user_router.router)
