from celery import Celery

from scraper.app import config

celery_app = Celery(backend=config.REDIS_URI, broker=config.REDIS_URI)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(config.SCRAPING_SCHEDULE_IN_HOURS, periodic_scraping.s(), name='scrape every N hours')


@celery_app.task(name='periodic_scraping')
def periodic_scraping():
    pass
