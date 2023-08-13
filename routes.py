from main import *

from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

# Root route that runs every 30 seconds.
@app.on_event("startup")
@repeat_every(seconds=30)
# Running after every 2 hours.
# @repeat_every(seconds=60*120)
@app.get("/")
async def root():
    return {"200": "success"}