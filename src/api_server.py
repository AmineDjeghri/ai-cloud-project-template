import os
from fastapi import FastAPI

# this should alway be on the top of the file
# server will always start from the directory where this file is located
os.chdir(os.path.dirname(__file__))

from log_config import LOGGING_CONFIG
from utils import logger, settings


import uvicorn
from api_route import router, TagEnum
from fastapi.responses import JSONResponse

app = FastAPI()

# ROUTERS
routers = [router]
for router in routers:
    app.include_router(router)


@app.get("/", tags=[TagEnum.general])
async def root():
    logger.debug("Server is up and running!")

    logger.debug(f"Settings: {settings}")

    return JSONResponse(content="server is up and running!")


if __name__ == "__main__":
    if settings.DEV_MODE:
        logger.info("Running app in DEV mode")
        reload = True
        LOGGING_CONFIG["loggers"]["uvicorn"]["level"] = "DEBUG"
        LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = "DEBUG"
        LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = "DEBUG"
    else:
        logger.info("Running app in PROD mode")
        reload = False
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(
        app=f"{module_name}:app",
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        reload=reload,
        log_config=LOGGING_CONFIG,
    )
