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

    def get_plain_text(self):
        return f"{os.path.basename(self.path)}\n"

    def get_contents(self):
        try:
            with open(self.path) as file:
                return file.read(), 200, "OK"
        except FileNotFoundError:
            return "File not found.", 404, "Not Found"
        except IsADirectoryError:
            return "You cannot read a directory's contents. Well, technically you can. But I won't allow it.", 400, "Bad Request"
        except NotADirectoryError:
            return "Where do you think you're going?", 400, "Bad Request"

    def write(self, content):
        try:
            message = "overwrote" if os.path.exists(self.path) else "created and wrote to"
            with open(self.path, 'w') as file:
                file.write(content)
                return f"Successfully {message} {os.path.basename(self.path)}. You can find it at {self.path}", 200, "OK"
        except IsADirectoryError:
            return "You cannot overwrite a directory's content.", 400, "Bad Request"
