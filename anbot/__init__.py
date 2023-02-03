import os
from celery import Celery

celery = Celery("tasks")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "pyamqp://rabbitmq:5672//")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://redis:6379"
)
celery.autodiscover_tasks(["anbot"])
