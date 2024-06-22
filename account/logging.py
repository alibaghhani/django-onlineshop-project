import logging




def log(func):
    logger = logging.getLogger(func.__module__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("account/authentication_system_logs.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(level-name)s - %(message)s'))
    file_handler.addFilter(CustomLogFilter())

    logger.addHandler(file_handler)

    def inner(*args, **kwargs):
        to_execute = func(*args, **kwargs)
        logging.basicConfig(level=logging.DEBUG, filename="account/authentication_system_logs.log", filemode="a")
        logging.info(f"entered into {func.__qualname__} with request {args=} and {kwargs=}")
        return to_execute

    return inner
