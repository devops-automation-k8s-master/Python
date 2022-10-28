"""Module to configure the Operation Handler dictionary"""

from metrics.porttest import porttest
from metrics.diskutil import diskutil
from metrics.memutil import memutil
opHandler = {
    "portTest": porttest,
    "diskUtil": diskutil,
    "memUtil" : memutil
}
