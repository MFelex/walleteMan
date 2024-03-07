from fastapi import status
from starlette.responses import JSONResponse


def ok(data=None):
    return JSONResponse(data, status_code=status.HTTP_200_OK)


def no_content(data):
    return JSONResponse(data, status_code=status.HTTP_204_NO_CONTENT)


def bad_request(data):
    return JSONResponse(data, status_code=status.HTTP_400_BAD_REQUEST)


def created(data):
    return JSONResponse(data, status_code=status.HTTP_201_CREATED)


def unauthorized(data):
    return JSONResponse(data, status_code=status.HTTP_401_UNAUTHORIZED)


def forbidden(data):
    return JSONResponse(data, status_code=status.HTTP_403_FORBIDDEN)


def not_found(data):
    return JSONResponse(data, status_code=status.HTTP_404_NOT_FOUND)
