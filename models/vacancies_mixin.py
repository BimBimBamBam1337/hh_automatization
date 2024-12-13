from typing import Any
import aiohttp


from tools import UniversalLogger


logger = UniversalLogger("managers_vacencies")


class VacanciesMixin:

    async def get_vacancies(
        self, url: str, employer_id: str, headers: dict
    ) -> list[dict[str, Any]]:
        try:
            url = url + f"vacancies?employer_id={employer_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        vacancies_json = await response.json()
                        vacancies_data = vacancies_json.get("items")
                        vacancies_list = [
                            {"vacancy_id": item["id"], "name": item["name"]}
                            for item in vacancies_data
                        ]
                        return vacancies_list
                    else:
                        print(await response.json())
                        logger.error(
                            f"An error has occurred:{response.status}",
                            extra="vacencies",
                        )
        except Exception as e:
            logger.error(f"An error has occurred: {e}", extra="vacencies")
