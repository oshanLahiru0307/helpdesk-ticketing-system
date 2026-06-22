from fastapi import FastAPI

from Config.Database import Base, engine
from Routes.AuthRoutes import router as auth_router
from Routes.UserRoutes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Help Desk API",
    description="Help Desk API with JWT authentication",
)

# Register route modules
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {"message": "Welcome to the Help Desk API!"}
