from fastapi import FastAPI
from app.routers.user_routers import router as user_router
from app.routers.code_routers import router as code_router



app = FastAPI(debug=True)

app.include_router(user_router)
app.include_router(code_router)
















