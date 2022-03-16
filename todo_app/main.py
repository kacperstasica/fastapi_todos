import uvicorn
from fastapi import FastAPI, status, Depends
from starlette.staticfiles import StaticFiles

import models
from database import engine
from routers import auth, todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
