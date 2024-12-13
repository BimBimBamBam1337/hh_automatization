import asyncio
from functools import wraps


from .univrsal_logger import UniversalLogger


logger = UniversalLogger("decorators")


def repeat(interval: int = 60):
    """
    Декоратор для повторного выполнения асинхронной функции с заданным интервалом.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            while True:
                try:
                    result = await func(*args, **kwargs)
                    if result:
                        logger.info(f"Updated data: {result}", extra="repeat")
                    else:
                        logger.warning(
                            "No data returned by the function", extra="repeat"
                        )
                except Exception as e:
                    logger.error(
                        f"An error occurred during the repeat function: {e}",
                        extra="repeat",
                    )
                await asyncio.sleep(interval)

        return wrapper

    return decorator
