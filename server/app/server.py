from fastapi import FastAPI
from .api.stac import sentinel2

app = FastAPI()

app.include_router(
    sentinel2.router,
    prefix='/api/stac/sentinel2',
    tags=["Sentinel 2 resource v1"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
