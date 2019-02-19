import os
from collections import OrderedDict


class Directory:

    def __init__(self, path: str, children: list):
        self.path = path
        self.children = children

    def __repr__(self):
        return OrderedDict(
            file=os.path.basename(self.path),
            isDir=True,
            children=self.children
        )

    def get_html(self):
        return f"<li>" \
            f"{os.path.basename(self.path)}" \
            f"<ul>" \
            f"{''.join(['<li>' + child.path + '</li>' for child in self.children])}" \
            f"</ul>" \
            f"</li>"
