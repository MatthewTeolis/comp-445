import re


class HttpRequest:

    def __init__(self, verb: str, path: str, version: str, qparams: dict, headers: dict, content: str):
        self.verb = verb

        path = path.replace('..', '')
        path = re.sub(r'/+', '/', path)
        self.path = path

        self.version = version
        self.qparams = qparams
        self.headers = headers
        self.content = content

    def __str__(self):
        return f'HttpRequest({self.verb}, {self.path}, {self.content})'
