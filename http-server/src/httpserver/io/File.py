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
