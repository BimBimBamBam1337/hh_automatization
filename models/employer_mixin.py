import aiohttp


from tools import UniversalLogger

logger = UniversalLogger("employer_mixin")


class EmployerMixin:
    ENDPOINT: str = "me"

    async def get_employer_id(self, url: str, headers: dict) -> str:
        try:
            url = url + self.ENDPOINT
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("employer", {}).get("id")
                    else:
                        logger.error(
                            f"An error has occurred:{response.status}",
                            extra="http_contection",
                        )
        except Exception as e:
            logger.error(f"An error has occurred: {e}", extra="http_conection")
