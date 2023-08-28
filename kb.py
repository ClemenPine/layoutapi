import json
import glob
from pathlib import Path
from dataclasses import dataclass

import classify, corpora

BIGRAMS = corpora.bigrams()

@dataclass(frozen=True)
class Position:
    row: int = 0
    col: int = 0
    finger: int = 0
    hand: int = 0

class Layout:
    name: str
    source: str
    authors: list[str]
    key: dict[str, Position]

    def __init__(self, file: str):
        with open(file, 'r') as f:
            data = json.load(f)

        self.name = Path(file).stem
        self.source = data['meta']['source']
        self.authors = data['meta']['authors']

        self.key = {}
        
        for key, path in paths(data['keys']):
            if 'pinky' in path:
                finger = 0
            if 'ring' in path:
                finger = 1
            if 'middle' in path:
                finger = 2
            if 'index' in path:
                finger = 3
            if 'thumb' in path:
                finger = 4

            if 'left' in path:
                hand = 0
            if 'right' in path:
                hand = 1

            pos = Position(
                [int(x[3:]) for x in path if x.startswith('row')][0],
                [int(x[3:]) for x in path if x.startswith('col')][0],
                finger,
                hand,
            )

            self.key[key] = pos

    def pos(self, gram: str):
        return [self.key[x] for x in gram]

    def metric(self, stat: str):
        func = getattr(classify, stat)

        score = 0
        total = 0

        for gram, count in BIGRAMS.items():
            if not all(x in self.key for x in gram):
                continue

            if func(self.pos(gram)):
                score += count

            total += count

        return score / total * 100

def paths(input_dict: dict):
    res: list[tuple[str, list[str]]] = []

    for key, value in input_dict.items():
        if isinstance(value, dict):
            for subkey, subval in paths(value):
                res.append((subkey, subval + [key]))
        else:
            res.append((value, [key]))

    return res

def layouts():
    files = glob.glob('layouts/*.json')
    files.sort()

    for file in files:
        yield Layout(file)