from dotenv import load_dotenv

load_dotenv()

from router.routes import api_router
from core.settings import settings

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title=settings.APP_NAME)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

app.include_router(api_router, prefix="/api")
