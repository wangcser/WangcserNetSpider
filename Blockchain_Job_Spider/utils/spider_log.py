import logging


logging.basicConfig(level=logging.INFO,
                    filename='../zhipin/zhipin_spider.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s: %(module)s %(message)s')
logger = logging.getLogger(__name__)

logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')