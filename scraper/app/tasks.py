import asyncio

from celery import Celery

from app import config, pull_repo
celery_app = Celery(backend=config.REDIS_URI, broker=config.REDIS_URI)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(int(config.SCRAPING_SCHEDULE_IN_MINUTES) * 60, periodic_scraping.s(),
                             name='scrape every N minutes')


@celery_app.task(name='periodic_scraping')
def periodic_scraping():
    asyncio.get_event_loop().run_until_complete(pull_repo.main())
