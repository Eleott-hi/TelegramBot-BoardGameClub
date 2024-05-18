import services.utils as utils

from fastapi import status, HTTPException
from config import MAIL_SERVICE_URL
from httpx import AsyncClient, Response


class MailService:

    def __init__(self):
        self.url = MAIL_SERVICE_URL

    async def send_token(self, email, token):
        async with AsyncClient() as client:
            res = await client.post(
                self.url + "/send_email",
                json={
                    "email": email,
                    "subject": "Confirm registration",
                    "message": f"Token:\n{token}",
                },
                timeout=10,
            )

            if res.status_code != status.HTTP_202_ACCEPTED:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail=utils.get_fastapi_error_detail(res.text),
                )