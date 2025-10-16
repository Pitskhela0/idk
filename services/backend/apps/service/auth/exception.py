from fastapi import status

from apps.infra.application.exception import BadRequestError


class AuthServiceError(BadRequestError):
    ...


class InvalidCredentialError(AuthServiceError):
    ...


class InvalidTokenError(InvalidCredentialError):
    status_code = status.HTTP_401_UNAUTHORIZED
