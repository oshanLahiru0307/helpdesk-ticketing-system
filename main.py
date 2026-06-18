from fastapi import FastAPI
from Config.Database import Base, engine

Base.metadata.create_all(bind=engine)




app = FastAPI(
    title="Help Desk API",
)

@app.get("/")
def home():
    return {"message": "Welcome to the Help Desk API!"}