from typing import Dict, Any


class GeneralTree:
    def __init__(self):
        self.AdjList: Dict[Any, list[Any]] = {}

    def append(self, p, c):
        if not self.AdjList:
            self.AdjList[p] = [c]
            self.AdjList[c] = []
            return

        if p not in self.AdjList:
            raise ValueError('The parent isn´t in the tree')

        self.AdjList[p] += [c]
        self.AdjList[c] = []

    def __repr__(self):
        return str(self.AdjList)


def bfs(gt: GeneralTree):
    if not gt:
        return 'The tree is empty'

    root = next(iter(gt.AdjList))
    pv = [(root, 1)]
    account = {}

    while pv:
        current = pv.pop(0)
        if current[1] not in account:
            account[current[1]] = current[0]
        else:
            account[current[1]] += current[0]

        if gt.AdjList[current[0]]:
            for i in gt.AdjList[current[0]]:
               pv.append((i, current[1]+1))
    return account

gt = GeneralTree()

gt.append('A', 'B')
gt.append('A', 'C')
gt.append('B', 'G')
print(bfs(gt))