from sortedcontainers import SortedDict


class Switch:

    rules: SortedDict

    def __init__(self):
        self.rules = SortedDict()
