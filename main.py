import asyncio
from models import BaseHHAPI, GoogleSheets
from tools import UniversalLogger, merge_data


logger = UniversalLogger("update_sheets")


async def update_sheets():
    logger.info("Запуск обновления данных.", extra="update_sheets")
    base = BaseHHAPI()
    google_sheets = GoogleSheets()
    try:
        result = await base.get_info()
        merged_data = merge_data(result[1], result[2])
        await google_sheets.create_and_fill_sheets(result[0], merged_data)
        logger.info("Обновление успешно завершено.", extra="update_sheets")
    except Exception as e:
        logger.error(f"Ошибка во время обновления: {e}", extra="update_sheets")


async def main():
    while True:
        try:
            await update_sheets()
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}", extra="main")
        await asyncio.sleep(30)  # Повтор через 5 минут


if __name__ == "__main__":
    asyncio.run(main())
