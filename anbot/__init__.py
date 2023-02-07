import os
import sqlalchemy as sa
from celery import Celery

# define our sqlite caches -- most of the bot's reporting and interactions
# are served out of the memory cache. The persistent cache just serves as a
# ledger for all message transmitted
sqlite_memory_cache = sa.create_engine("sqlite:///")
sqlite_persistent_cache = sa.create_engine("sqlite:///data/cache.sqlite")
# celery tasks backend
celery = Celery("tasks")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "pyamqp://rabbitmq:5672//")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://redis:6379"
)
celery.autodiscover_tasks(["anbot"])
