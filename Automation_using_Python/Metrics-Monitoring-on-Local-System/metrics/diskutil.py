"""This program calculate disk utilization of loca system on given mounted path."""
import os
import psutil
import logging

logger = logging.getLogger("diskUtil")
def diskutil(config):
    diskPath=config["diskUtil"]
    print(diskPath)
    try:
        diskUsage=psutil.disk_usage(diskPath).percent
        logger.debug("{}% system disk utilization\n".format(diskUsage))
    except:
        logger.debug(" No disk on this  path:{} so please check your path".format(diskPath))
