from __future__ import print_function

import os
from threading import Timer

import redis
from util import s3
from bluelens_log import Logging

HEALTH_CHECK_TIME = 60*20
TEXT_CLASSIFICATION_MODEL_FILE = 'cooking.bin'

AWS_MODEL_BUCKET = 'bluelens-style-model'
AWS_BUCKET_CLASSIFICATION_TEXT_PATH = 'classification/text/'

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY'].replace('"', '')
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'].replace('"', '')

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-text-classifier')
rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)
storage = s3.S3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

def upload_text_model_file():
  log.info('upload_text_model_file')
  file = os.path.join(os.getcwd(), TEXT_CLASSIFICATION_MODEL_FILE)
  print(file)
  try:
    return storage.upload_file_to_bucket(AWS_MODEL_BUCKET, file, AWS_BUCKET_CLASSIFICATION_TEXT_PATH + TEXT_CLASSIFICATION_MODEL_FILE)
  except:
    log.error('upload error')
    return None

def download_text_model_file():
  log.info('download_text_model_file')
  file = os.path.join(os.getcwd(), TEXT_CLASSIFICATION_MODEL_FILE)
  try:
    return storage.download_file_from_bucket(AWS_MODEL_BUCKET, file, AWS_BUCKET_CLASSIFICATION_TEXT_PATH + TEXT_CLASSIFICATION_MODEL_FILE)
  except:
    log.error('download error')
    return None

"""
#Redis health check
def check_health():
  global  heart_bit
  log.info('check_health: ' + str(heart_bit))
  if heart_bit == True:
    heart_bit = False
    Timer(HEALTH_CHECK_TIME, check_health, ()).start()
  else:
    delete_pod()
      
def delete_pod():
  log.info('exit: ' + SPAWN_ID)

  data = {}
  data['namespace'] = RELEASE_MODE
  data['key'] = 'SPAWN_ID'
  data['value'] = SPAWN_ID
  spawn = spawning_pool.SpawningPool()
  spawn.setServerUrl(REDIS_SERVER)
  spawn.setServerPassword(REDIS_PASSWORD)
  spawn.delete(data)
"""

def start(rconn):
  # global version_id

  # upload text model file to s3
  # print(upload_text_model_file())

  # 1. Checking redis health
  # Timer(HEALTH_CHECK_TIME, check_health, ()).start()
  count = 0

  # 2. download text classification model from s3
  print(download_text_model_file())

  # 3. Checking redis queue
  # while True:
  #   key, value = rconn.blpop([REDIS_PRODUCT_CLASSIFY_QUEUE])
  #   if value is not None:
  #     analyze_product(value)
  #   global  heart_bit
  #   heart_bit = True

if __name__ == '__main__':
  try:
    log.info('Start bl-text-classifier')
    start(rconn)
  except Exception as e:
    log.error(str(e))
