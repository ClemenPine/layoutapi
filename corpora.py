import json

def monograms():
    return load('monograms')

def bigrams():
    return load('bigrams')

def skipgrams():
    return load('skipgrams')

def load(name: str, corpora: str='monkeyracer'):
    with open(f'corpora/{corpora}/{name}.json', 'r') as f:
            data: dict[str, int] = json.load(f)

    return data