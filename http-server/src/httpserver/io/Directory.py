import os
from collections import OrderedDict


class Directory:

    def __init__(self, path: str, children: iter):
        self.path = path
        self.children = children

    def __repr__(self):
        return OrderedDict(
            file=os.path.basename(self.path),
            isDir=True,
            children=[child.__repr__() for child in self.children]
        )

    def get_html(self):
        return f"<li>" \
            f"{os.path.basename(self.path)}" \
            f"<ul>" \
            f"{''.join([child.get_html() for child in self.children])}" \
            f"</ul>" \
            f"</li>"
