class HttpRequest:

    def __init__(self, verb: str, path: str, version: str, headers: dict, content: str):
        self.verb = verb
        self.path = path
        self.version = version
        self.headers = headers
        self.content = content
