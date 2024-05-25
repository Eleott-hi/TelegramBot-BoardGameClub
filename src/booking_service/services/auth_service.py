import httpx

from fastapi import HTTPException, logger, status

from config import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_VERSION
from schemas.schemas import User
from services import utils


class AuthService:
    def __init__(self):
        self.auth_url = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/api/v{AUTH_SERVICE_VERSION}"

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        url = f"{self.auth_url}/user"
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)

            if response.status_code == 200:
                return User.model_validate_json(response.text)

            err = utils.get_fastapi_error(response)
            print(err)
            raise err


        except httpx.TimeoutException as err:
            print(err)
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
