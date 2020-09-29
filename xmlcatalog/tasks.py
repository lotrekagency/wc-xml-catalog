import settings
from service import create_xml
from huey import RedisHuey, crontab

huey = RedisHuey('feedXML', host=settings.REDIS_HOST)

@huey.periodic_task(crontab(minute='0', hour=settings.CRONTAB_HOUR))
def task():
    create_xml()

