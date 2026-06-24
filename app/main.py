from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from Config.database import Base, engine
from controllers.auth_controller import router as auth_router
from controllers.user_controller import router as user_router
from core.exceptions import AppException

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Help Desk API",
    description="Help Desk API with JWT authentication",
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {"message": "Welcome to the Help Desk API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)