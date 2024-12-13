from .resume_mixin import ResumeMixin
from tools import UniversalLogger, repeat
from .invitation_mixin import InvitationMixin
from .http_mixin import HttpRequestMixin
from .employer_mixin import EmployerMixin
from .vacancies_mixin import VacanciesMixin
import asyncio


logger = UniversalLogger("base_api")


class BaseHHAPI(
    HttpRequestMixin, EmployerMixin, VacanciesMixin, InvitationMixin, ResumeMixin
):
    """Базовый класс для работы с API HeadHunter, объединяющий функциональность миксинов."""

    async def get_info(self) -> list:
        """
        Основной метод для получения информации: вакансии, приглашения и резюме.

        Returns:
            list: Список, содержащий данные о вакансиях, приглашениях и резюме.
        """
        try:
            # Получение идентификатора работодателя
            employer_id = await self.get_employer_id(
                self.base_url, headers=self.headers
            )
            logger.info(f"Получен ID работодателя: {employer_id}", extra="base_api")

            # Последовательное выполнение запросов
            vacancies = await self.get_vacancies(
                url=self.base_url,
                employer_id=employer_id,
                headers=self.headers,
            )
            logger.info(f"Получено {len(vacancies)} вакансий", extra="base_api")

            # Передача вакансий для получения приглашений
            invitations = await self.get_invitations(
                url=self.base_url,
                headers=self.headers,
                vacancies=vacancies,
            )
            logger.info(f"Получено {len(invitations)} приглашений", extra="base_api")

            # Передача приглашений для получения резюме
            resumes = await self.get_resumes(
                url=self.base_url,
                invitations=invitations,
                headers=self.headers,
            )
            logger.info(f"Получено {len(resumes)} резюме", extra="base_api")

            return [vacancies, invitations, resumes]

        except Exception as e:
            logger.error(f"Ошибка при выполнении get_info: {e}", extra="base_api")
            return []
