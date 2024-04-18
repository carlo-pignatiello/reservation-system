from app.logger import logger


def retry(times, exceptions):
    """_summary_

    Args:
        times (_type_): _description_
        exceptions (_type_): _description_
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    logger.info(f"Attemp: {attempt}/{times}")
                    return func(*args, **kwargs)
                except exceptions:
                    logger.info(
                        "Exception thrown when attempting to run %s, attempt "
                        "%d of %d" % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator
