"""This is a main driver program which reads the configuration and check for the
configured metrics
"""
import json
import logging
import metrics
import time
import logging.config

with open('config.json') as cf:
    config = json.load(cf)

if 'logging-config' in config:
    logging.config.dictConfig(config['logging-config'])
else:
    logging.basicConfig(level=logging.DEBUG)

logging.info('Application Started')
logging.debug('Metrics Registered: {}'.format(metrics.opHandler.keys()))

while True:
    metrices=config["monitoring-metrics"]
    for i in metrices:
        metrics.opHandler[i](config)
        time.sleep(config['interval'])


logging.info('Application Ended')
