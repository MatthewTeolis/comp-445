import os
from collections import OrderedDict


class Directory:

    def __init__(self, path: str, children: iter, depth: int):
        self.path = path
        self.children = children
        self.depth = depth

    def __repr__(self):
        return OrderedDict(
            file=os.path.basename(self.path),
            isDir=True,
            children=[child.__repr__() for child in self.children]
        )

    def get_html(self):
        return f"<li>" \
            f"{os.path.basename(self.path)}" \
            f"<ul style='margin: 0'>" \
            f"{''.join([child.get_html() for child in self.children])}" \
            f"</ul>" \
            f"</li>"

    def get_plain_text(self):
        directory = f"{os.path.basename(self.path)}\n"
        files = [self.depth * "\t" + child.get_plain_text() for child in self.children]
        return directory + ''.join(files)
