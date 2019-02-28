class HttpResponse:

    def __init__(self, version: str, code: int, status: str, headers: dict, body: str):
        self.version = version
        self.code = code
        self.status = status
        self.headers = headers
        self.body = body

    def get_status_line(self):
        return f'{self.version} {self.code} {self.status}'

    def stringify_headers(self):
        return '\r\n'.join(f'{key}: {value}' for key, value in self.headers.items())

    def __repr__(self):
        return f"{self.get_status_line()}\r\n{self.stringify_headers()}\r\n\r\n{self.body}\r\n\r\n"
