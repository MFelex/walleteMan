from celery import Celery

from wallet.core.config import env


def create_celery_app() -> Celery:
    app_ = Celery(
        'wallet',
        broker=env.BROKER_URL,
        include=['wallet.tasks.worker']
    )

    app.conf.task_routes = {
        'withdraw.request': {'queue': 'withdraw.request'},
        'withdraw.action': {'queue': 'withdraw.action'},

    }
    app.conf.update(
        result_expires=3600,
    )

    app.autodiscover_tasks([
        'wallet.tasks'
    ])

    return app_


app = create_celery_app()
