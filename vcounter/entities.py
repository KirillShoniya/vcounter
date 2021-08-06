

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int = None, payload: dict = None):
        Exception.__init__(self)
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self) -> dict:
        error_info = dict(self.payload or ())
        error_info['status'] = 'error'
        error_info['message'] = self.message
        return error_info
