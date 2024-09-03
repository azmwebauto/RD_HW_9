import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app import cves, config

app = FastAPI()
app.include_router(cves.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/status")
async def get_status():
    return 'OK'


if __name__ == '__main__':
    uvicorn.run('app.main:app', host=config.HOST, port=config.PORT)
