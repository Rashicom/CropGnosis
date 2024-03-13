from rest_framework.exceptions import APIException

class CustomAPIException(APIException):
    def __init__(self, detail, status_code=None):
        self.detail = {"error": detail}
        self.status_code = status_code or 400


class BadRequestException(CustomAPIException):
    def __init__(self, detail="Bad Request.", status_code=400):
        super().__init__(detail, status_code)


class NotAcceptableException(CustomAPIException):
    def __init__(self, detail="Parameter unacceptable.", status_code=406):
        super().__init__(detail, status_code)


class UnauthorizedException(CustomAPIException):
    def __init__(self, detail="Access Denied.", status_code=401):
        super().__init__(detail, status_code)


class PermissionDeniedException(CustomAPIException):
    def __init__(self, detail="Permission Denied.", status_code=403):
        super().__init__(detail, status_code)


class NotFoundException(CustomAPIException):
    def __init__(self, detail="Not found.", status_code=404):
        super().__init__(detail, status_code)


class UnsupportedMediaTypeException(CustomAPIException):
    def __init__(self, detail="Unsupported media type .", status_code=415):
        super().__init__(detail, status_code)


class ConflictException(CustomAPIException):
    def __init__(self, detail="Conflict.", status_code=409):
        super().__init__(detail, status_code)


class UnhandledException(CustomAPIException):
    def __init__(self, detail="Unhandled exception.", status_code=500):
        super().__init__(detail, status_code)