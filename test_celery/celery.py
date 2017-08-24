from __future__ import absolute_import
from celery import Celery

machineIP = "172.16.0.2"
app = Celery('test_celery', broker='amqp://admin:mypass@{}:5672'.format(machineIP), 
              backend='rpc://', include=['test_celery.tasks'])


