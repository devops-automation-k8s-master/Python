"""This program calculate memory utilization of local systems"""
import psutil
import logging

logger = logging.getLogger("memUtil")
def memutil(config):

    monitorQuery=config["memUtil"]
    if monitorQuery=="system":
        data=psutil.virtual_memory().percent
        logger.debug("{}% system memory utilization".format(data))
    else:
        logger.debug("please set memMonitoring variable to system")
