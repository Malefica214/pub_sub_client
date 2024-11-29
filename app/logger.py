import logging, os

def setup_logger():
    #logger
    log_level = os.environ.get('LOG_LEVEL') or 'INFO'
    log = logging.getLogger("bean_logger")
    log.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s]: [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s"
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)
    
    return log