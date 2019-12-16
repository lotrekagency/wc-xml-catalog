from service import create_xml
from settings import REDIS_HOST
from huey import RedisHuey, crontab

huey = RedisHuey('feedXML', host=REDIS_HOST)

@huey.periodic_task(crontab(minute='0', hour='*/7'))
def task():
    create_xml()

