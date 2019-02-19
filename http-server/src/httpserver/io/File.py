import os
from collections import OrderedDict


class File:

    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return OrderedDict(
            file=os.path.basename(self.path),
            isDir=False
        )

    def get_html(self):
        return f"<li>{os.path.basename(self.path)}</li>"

    def get_contents(self):
        try:
            return open(self.path).read(), 200, "OK"
        except FileNotFoundError:
            return "File not found.", 404, "Not Found"
        except IsADirectoryError:
            return "You cannot read a directory's contents. Well, technically you can. But I won't allow it.", 400, "Bad Request"
        except NotADirectoryError:
            return "Where do you think you're going?", 400, "Bad Request"
