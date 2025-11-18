import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.v1 import auth, users, admin_acl

app = FastAPI(
    title='test API',
    description='API для тестового задания',
    version='0.1.0',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin_acl.router)


async def start_app():
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level='info',
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(start_app())