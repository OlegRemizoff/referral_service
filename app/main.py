from fastapi import FastAPI, Query, Depends
from app.routers import user_router



app = FastAPI(debug=True)

app.include_router(user_router)
















