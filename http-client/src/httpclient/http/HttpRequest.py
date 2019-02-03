class HttpRequest:

    def __init__(self, host: str, port: int, type: str, path: str,
                 headers: dict = None, data: str = None, version: str = 'HTTP/1.0'):
        if headers is None:
            headers = {}
        self.host = host
        self.port = port
        self.type = type
        self.path = path
        self.headers = headers
        self.data = data
        self.version = version

    def get_request_line(self):
        return f'{self.type} {self.path} {self.version}'

    def stringify_headers(self):
        return '\r\n'.join(f'{key}: {value}' for key, value in self.headers.items())

    def __repr__(self):
        build = [self.get_request_line()]

        if len(self.headers) != 0:
            build.append(self.stringify_headers())

        if self.data is not None:
            build.append('')
            build.append(self.data)

        return '\r\n'.join(build) + '\r\n\r\n'
