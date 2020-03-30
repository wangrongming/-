import logging


def one():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode='a',
        filename='outer.log',
    )
    logger = logging.getLogger(__name__)

    logger.info(__name__)
    logger.info('This is a log info')
    logger.debug('Debugging')
    logger.warning('Warning exists')


def two():
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)

    # StreamHandler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(stream_handler)

    # FileHandler
    file_handler = logging.FileHandler('output.log')
    file_handler.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log
    # logger.info('This is a log info')
    # logger.debug('Debugging')
    # logger.warning('Warning exists')
    # logger.info('Finish')
    try:
        result = 10 / 0
    except Exception as e:
        # logger.error(e, exc_info=True)  # exc_info=True 打印执行过程信息
        logger.info('error', extra={"extra": "额外参数测试"})  # exc_info=True 打印执行过程信息


if __name__ == '__main__':
    two()
