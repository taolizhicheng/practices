import logging


__all__ = ["get_logger"]
def __dir__():
    return __all__


def get_logger(
    logger_name: str,
    level: int = logging.DEBUG,
    fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file: str = None,
):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # 创建一个处理器
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # 创建一个格式化器
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    if log_file is not None:
        # 创建一个文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # 创建一个格式化器
        formatter = logging.Formatter(fmt)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
