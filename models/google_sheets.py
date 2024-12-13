import asyncio
import gspread
from typing import List, Dict
from tools import UniversalLogger, repeat

logger = UniversalLogger("google_sheets")


class GoogleSheets:
    def __init__(self):
        try:
            logger.info("Инициализация GoogleSheets", extra="google")
            self.gc = gspread.service_account(filename="credentials.json")
            self.sh = self.gc.open_by_key(
                "1Me8j4VGsX78SxCg8FuGC4fXMYs72OGJMN8hzhkFBHxY"
            )
            logger.info("Успешное подключение к таблице", extra="google")
        except Exception as e:
            logger.error(f"Ошибка при инициализации GoogleSheets: {e}", extra="google")
            raise

    async def create_and_fill_sheets(self, vacancies: list[dict], data: list[dict]):
        logger.info(f"Входные данные для вакансий: {vacancies}", extra="google")
        logger.info(f"Входные данные для приглашений: {data}", extra="google")

        headers = [
            "№",
            "Дата",
            "Запрос",
            "Источник",
            "ФИО",
            "Предмет",
            "Возраст",
            "Языки",
            "Телефон",
            "Тестирование",
            "Баллы",
            "Интервь назначено",
            "Дата интервью",
            "Время интервью",
            "Проведено",
            "Статус",
            "Причина отказа",
            "Дата переноса интервью",
            "Время переноса интервью",
            "Номер ГПХ",
        ]

        existing_sheets = {
            sheet.title: sheet for sheet in self.sh.worksheets()
        }  # Словарь существующих листов

        for vacancy in vacancies:
            vacancy_name = vacancy.get("name")
            vacancy_id = vacancy.get("vacancy_id")

            try:
                logger.info(
                    f"Обработка вакансии: {vacancy_name} (ID: {vacancy_id})",
                    extra="google",
                )

                # Создание или использование существующего листа
                if vacancy_name not in existing_sheets:
                    worksheet = self.sh.add_worksheet(
                        title=vacancy_name, rows=100, cols=20
                    )
                    worksheet.append_row(headers)
                    logger.info(
                        f"Лист '{vacancy_name}' создан и заголовки добавлены.",
                        extra="google",
                    )
                else:
                    worksheet = existing_sheets[vacancy_name]
                    logger.info(
                        f"Лист '{vacancy_name}' уже существует, данные будут добавлены.",
                        extra="google",
                    )

                # Получение всех существующих данных из листа
                existing_rows = worksheet.get_all_values()[1:]  # Пропускаем заголовки
                existing_identifiers = {
                    row[1] for row in existing_rows
                }  # Используем поле "Дата" как уникальный идентификатор

                # Фильтрация уникальных записей
                unique_rows = [
                    [
                        "",  # Пустое поле для номера
                        invitation.get("created_at"),  # Дата
                        "",  # Пустое поле для запроса
                        "",  # Пустое поле для источника
                        invitation.get("full_name"),  # ФИО
                        "",  # Пустое поле для предмета
                        invitation.get("age"),  # Возраст
                        "",  # Пустое поле для языков
                        invitation.get("phone_number"),  # Телефон
                        "",  # Пустое поле для тестирования
                        "",  # Пустое поле для баллов
                        "",  # Пустое поле для интервью
                        "",  # Пустое поле для даты интервью
                        "",  # Пустое поле для времени интервью
                        "",  # Пустое поле для проведено
                        "",  # Пустое поле для статуса
                        "",  # Пустое поле для причины отказа
                        "",  # Пустое поле для даты переноса интервью
                        "",  # Пустое поле для времени переноса интервью
                        "",  # Пустое поле для номера ГПХ
                    ]
                    for invitation in data
                    if invitation.get("vacancy_id") == vacancy_id
                    and invitation.get("created_at") not in existing_identifiers
                ]

                # Запись только уникальных строк
                if unique_rows:
                    worksheet.append_rows(unique_rows)
                    logger.info(
                        f"Добавлены {len(unique_rows)} уникальные записи в лист '{vacancy_name}'.",
                        extra="google",
                    )
                else:
                    logger.info(
                        f"Для вакансии '{vacancy_name}' нет уникальных записей для добавления.",
                        extra="google",
                    )

            except Exception as e:
                logger.error(
                    f"Ошибка при обработке вакансии '{vacancy_name}': {e}",
                    extra="google",
                )
