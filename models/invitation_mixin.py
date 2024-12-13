import aiohttp
from datetime import datetime
from typing import Any, Dict, List
from tools import UniversalLogger

logger = UniversalLogger("invitation_mixin")


class InvitationMixin:
    async def _get_collections(
        self, url: str, headers: Dict[str, str], vacancies: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        async with aiohttp.ClientSession() as session:
            all_collections = []  # Инициализация списка для всех коллекций
            for vacancy in vacancies:
                vacancy_id = vacancy.get("vacancy_id")
                if not vacancy_id:
                    logger.warning(
                        f"Vacancy ID is missing for {vacancy}", extra="vacancy_id"
                    )
                    continue

                # Формирование URL запроса
                request_url = f"{url}negotiations?vacancy_id={vacancy_id}&with_generated_collections=true"
                try:
                    async with session.get(request_url, headers=headers) as response:
                        if response.status != 200:
                            logger.error(
                                f"Failed to fetch negotiations: {response.status} for vacancy_id {vacancy_id}",
                                extra="vacancy_id",
                            )
                            continue  # Продолжаем, если ошибка при запросе
                        data = await response.json()
                        collections = data.get("collections")
                        for item in collections:
                            if item["id"] in [
                                "consider",
                                "phone_interview",
                                "interview",
                            ]:
                                all_collections.append(
                                    {"vacancy_id": vacancy_id, "url": item["url"]}
                                )
                except Exception as e:
                    logger.error(
                        f"Error during request: {str(e)} for vacancy_id {vacancy_id}",
                        extra="vacancy_id",
                    )
                    continue  # Обрабатываем исключения и продолжаем цикл
            return all_collections

    async def get_invitations(
        self, url: str, headers: dict, vacancies: list[dict[str, Any]]
    ):
        collections = await self._get_collections(
            url=url, headers=headers, vacancies=vacancies
        )
        all_invitations = []  # Список для хранения всех приглашений
        async with aiohttp.ClientSession() as session:
            for item in collections:
                try:
                    request_url = f"{item['url']}"
                    vacancy_id = item["vacancy_id"]
                    async with session.get(request_url, headers=headers) as response:
                        if response.status != 200:
                            logger.error(
                                f"Failed to fetch negotiations: {response.status} for {request_url}",
                                extra="vacancy_id",
                            )
                            break  # Прерываем, если ошибка при запросе

                        data = await response.json()
                        collection_items = data.get("items")
                        for item in collection_items:
                            if item["employer_state"].get("id") in [
                                "consider",
                                "phone_interview",
                                "interview",
                            ]:
                                first_name = (
                                    item["resume"].get("first_name", "Не указано") or ""
                                )
                                middle_name = (
                                    item["resume"].get("middle_name", "") or ""
                                )
                                last_name = (
                                    item["resume"].get("last_name", "Не указано") or ""
                                )

                                # Формируем полное имя, игнорируя пустое отчество
                                full_name = (
                                    f"{last_name} {first_name} {middle_name}".strip()
                                )

                                created_at = item.get("created_at", "Не указано") or ""
                                age = item["resume"].get("age", "Не указано") or ""
                                resume_id = (
                                    item.get("resume", {}).get("id", "Не указано") or ""
                                )
                                all_invitations.append(
                                    {
                                        "full_name": full_name,
                                        "created_at": datetime.strptime(
                                            created_at, "%Y-%m-%dT%H:%M:%S%z"
                                        ).strftime("%d.%m.%Y %H:%M"),
                                        "age": age,
                                        "resume_id": resume_id,
                                        "vacancy_id": vacancy_id,
                                    }
                                )
                except Exception as e:
                    logger.error(f"Error during request: {e}", extra="vacancy_id")
                    break  # Прерываем цикл при ошибке
        unique_data = {item["resume_id"]: item for item in all_invitations}
        unique_data = list(unique_data.values())

        logger.info(f"Fetched {len(all_invitations)} invitations.", extra="vacancy_id")
        return all_invitations
