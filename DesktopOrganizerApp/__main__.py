import re
import os
import sys
__file__ = "/Users/lan/Desktop/MonitorBucketMaker/MonitorBucket.py"
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from MonitorBucket import __MonitorBucket

if __name__ == "__main__.py":
    monitorBucket = __MonitorBucket()
