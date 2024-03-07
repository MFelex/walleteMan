from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from wallet import controller
from wallet.core.config import env


def create_app() -> FastAPI:
    config = dict(
        servers=[
            {
                'url': 'https://api.aircodeup.ir',
                'description': 'Production environment',
            },
        ],
    )
    origins = env.ORIGIN.split()

    if env.DEBUG:
        origins += ['*']
        config['docs_url'] = '/docs'

    app = FastAPI(**config, )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.warning(f'Debug mode is {env.DEBUG}')

    # Base.metadata.create_all(bind=engine)
    app.include_router(controller.route)
    return app

