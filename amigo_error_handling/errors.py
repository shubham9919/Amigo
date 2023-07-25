from flask import jsonify
from werkzeug.exceptions import HTTPException

'''Ref: https://werkzeug.palletsprojects.com/en/2.3.x/exceptions/'''

class NotFoundError(HTTPException):
    def __init__(self, description=None, code=404):
        # Initialization of the parent class (HTTPException).
        super().__init__()
        self.description = description or "Not Found"
        self.code = code or 404

class InternalServerError(HTTPException):
    def __init__(self, description=None, code=500):
        super().__init__()
        self.description = description or "Internal Server Error"
        self.code = code or 500

class BadRequestError(HTTPException):
    def __init__(self, description=None, code=400):
        super().__init__()
        self.description = description or "Bad Request"
        self.code = code or 400
    
class UnauthorizedError(HTTPException):
    def __init__(self, description=None, code=401):
        super().__init__()
        self.description = description or "Unauthorized"
        self.code = code or 401 

class ForbiddenError(HTTPException):
    def __init__(self, description=None, code=403):
        super().__init__()
        self.description = description or "Forbidden"
        self.code = code or 403

class MethodNotAllowedError(HTTPException):
    def __init__(self, description=None, code=405):
        super().__init__()
        self.description = description or "Method Not Allowed"
        self.code = code or 405

class NotAcceptableError(HTTPException):
    def __init__(self, description=None, code=406):
        super().__init__()
        self.description = description or "Not Acceptable"
        self.code = code or 406 

class RequestTimeoutError(HTTPException):
    def __init__(self, description=None, code=408):
        super().__init__()
        self.description = description or "Request Timeout"
        self.code = code or 408  

class ConflictError(HTTPException):
    def __init__(self, description=None, code=409):
        super().__init__()
        self.description = description or "Conflict"
        self.code = code or 409   


class GoneError(HTTPException):
    def __init__(self, description=None, code=410):
        super().__init__()
        self.description = description or "Gone"
        self.code = code or 410 

class LengthRequiredError(HTTPException):
    def __init__(self, description=None, code=411):
        super().__init__()
        self.description = description or "Length Required"
        self.code = code or 411  

class PreconditionFailedError(HTTPException):
    def __init__(self, description=None, code=412):
        super().__init__()
        self.description = description or "Precondition Failed"
        self.code = code or 412

class RequestEntityTooLargeError(HTTPException):
    def __init__(self, description=None, code=413):
        super().__init__()
        self.description = description or "Request Entity Too Large"
        self.code = code or 413

class RequestURITooLargeError(HTTPException):
    def __init__(self, description=None, code=414):
        super().__init__()
        self.description = description or "Request URI Too Large"
        self.code = code or 414

class UnsupportedMediaTypeError(HTTPException):
    def __init__(self, description=None, code=415):
        super().__init__()
        self.description = description or "Unsupported Media Type"
        self.code = code or 415

class RequestedRangeNotSatisfiableError(HTTPException):
    def __init__(self, description=None, code=416):
        super().__init__()
        self.description = description or "Requested Range Not Satisfiable"
        self.code = code or 416

class UnprocessableEntityError(HTTPException):
    def __init__(self, description=None, code=422):
        super().__init__()
        self.description = description or "Unprocessable Entity"
        self.code = code or 422

class LockedError(HTTPException):
    def __init__(self, description=None, code=423):
        super().__init__()
        self.description = description or "Locked"
        self.code = code or 423

class FailedDependencyError(HTTPException):
    def __init__(self, description=None, code=424):
        super().__init__()
        self.description = description or "Failed Dependency"
        self.code = code or 424

class PreconditionRequiredError(HTTPException):
    def __init__(self, description=None, code=428):
        super().__init__()
        self.description = description or "Precondition Required"
        self.code = code or 428

class TooManyRequestsError(HTTPException):
    def __init__(self, description=None, code=429):
        super().__init__()
        self.description = description or "Too Many Requests"
        self.code = code or 429

class RequestHeaderFieldsTooLargeError(HTTPException):
    def __init__(self, description=None, code=431):
        super().__init__()
        self.description = description or "Request Header Fields Too Large"
        self.code = code or 431

class UnavailableForLegalReasonsError(HTTPException):
    def __init__(self, description=None, code=451):
        super().__init__()
        self.description = description or "Unavailable For Legal Reasons"
        self.code = code or 429

class InternalServerError(HTTPException):
    def __init__(self, description=None, code=500):
        super().__init__()
        self.description = description or "Internal Server Error"
        self.code = code or 500

class NotImplementedError(HTTPException):
    def __init__(self, description=None, code=501 ):
        super().__init__()
        self.description = description or "Not Implemented"
        self.code = code or 501 

class BadGatewayError(HTTPException):
    def __init__(self, description=None, code=502):
        super().__init__()
        self.description = description or "Bad Gateway"
        self.code = code or 502 

class ServiceUnavailableError(HTTPException):
    def __init__(self, description=None, code=503):
        super().__init__()
        self.description = description or "Service Unavailable"
        self.code = code or 503

class GatewayTimeoutError(HTTPException):
    def __init__(self, description=None, code=504 ):
        super().__init__()
        self.description = description or "Gateway Timeout"
        self.code = code or 504 

class HTTPVersionNotSupportedError(HTTPException):
    def __init__(self, description=None, code=505):
        super().__init__()
        self.description = description or "HTTP Version Not Supported"
        self.code = code or 505

class ClientDisconnectedError(HTTPException):
    def __init__(self, description=None, code=504 ):
        super().__init__()
        self.description = description or "Gateway Timeout"
        self.code = code or 504 


class CustomError(HTTPException):
    def __init__(self, description=None, code=400):
        super().__init__()
        self.description = description or "Custom Error"
        self.code = code

def handle_error(error):
    response = {
        "error": {
            "code": error.code,
            "message": error.description
        }
    }
    return jsonify(response), error.code