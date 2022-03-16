import uvicorn
from fastapi import FastAPI, status

import models
from database import engine
from routers import auth, todos
from company import companyapis


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
# external routing - we add prefixes, tags and responses unique to our app, not to the APIs
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    responses={status.HTTP_418_IM_A_TEAPOT: {"description": "Internal Use Only"}}
)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
