import logging
logger = logging.getLogger('uvcsite.nva.accordion')

def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)
