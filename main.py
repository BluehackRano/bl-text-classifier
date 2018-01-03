from __future__ import print_function

import os
import redis
from bluelens_log import Logging


REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-image-processor')
rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)

if __name__ == '__main__':
  try:
    log.info('Start bl-image-processor:7')
  except Exception as e:
    log.error(str(e))
