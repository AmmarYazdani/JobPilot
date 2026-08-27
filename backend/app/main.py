from sqlalchemy import text

from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.database.database import engine
from app.api.routes.resume import router as resume_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(resume_router)


@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.get("/db-test")
def db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        return{"status": "connected"}
