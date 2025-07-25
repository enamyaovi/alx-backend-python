
import logging
import os
from typing import Any
from datetime import datetime, time
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='requests.log', mode='a', encoding="utf-8")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("{asctime} - {levelname}: {message}", style="{")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request,*args: Any, **kwds: Any) -> Any:

        response = self.get_response(request)
        user = request.user
        logger.info(msg=f"{datetime.now()} - User: {user} - Path: {request.path}")

        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request,*args: Any, **kwargs: Any) -> Any:
        
        current_time = datetime.now().time()

        before = time(hour=18,minute=00) #type: ignore
        after = time(hour=21, minute=00) #type: ignore

        if current_time < before or current_time > after:
            raise PermissionDenied
            # return JsonResponse(
                # {"message": "Sorry, chatroom API is closed."},
                # status=403
            # )

        return self.get_response(request)