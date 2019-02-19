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
