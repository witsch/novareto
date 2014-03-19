import logging
logger = logging.getLogger('uvcsite.nva.flgdesktop')

def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)
