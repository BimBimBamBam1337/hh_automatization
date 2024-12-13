import aiohttp
from tools import UniversalLogger

logger = UniversalLogger("resume")


class ResumeMixin:
    async def get_resumes(self, url: str, invitations: list[dict], headers: dict):
        async with aiohttp.ClientSession() as session:
            resumes = []
            for data in invitations:
                resume_id, vacancy_id = data.get("resume_id"), data.get("vacancy_id")
                if not resume_id:
                    continue
                try:
                    async with session.get(
                        f"{url}resumes/{resume_id}", headers=headers
                    ) as response:
                        if response.status == 200:
                            resume_data = await response.json()
                            resumes.append(
                                {
                                    "vacancy_id": vacancy_id,
                                    "resume_id": resume_id,
                                    "phone_number": resume_data.get("contact", [{}])[0]
                                    .get("value", {})
                                    .get("formatted", ""),
                                }
                            )
                        else:
                            logger.error(
                                f"Failed to fetch resume {resume_id}: {response.status}",
                                extra="resume",
                            )
                except Exception as e:
                    logger.error(
                        f"Error fetching resume {resume_id}: {e}", extra="resume"
                    )
        return resumes
