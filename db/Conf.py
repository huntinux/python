# -*- coding: utf-8 *-

import os
import logging

this_dir, this_filename = os.path.split(__file__)

# 本地redis
redis = {
    'host': '127.0.0.1',
    'port': 6379
}

remoteRedis = {
    'host': 'xxxxxxxxxxxx',
    'port': 6379
}

# 远程redis
def getLogger():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',\
            level=logging.DEBUG, filename = '/tmp/InterLowprice.log')

    return logging.getLogger('InterLowprice')

if __name__ == '__main__':
    pass
