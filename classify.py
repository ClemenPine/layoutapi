import kb

def rlb(key: 'list[kb.Position]'):
    return len(set(key)) == 1

def sfb(key: 'list[kb.Position]'):
    return (
        not rlb(key) and
        len(set((x.finger for x in key))) == 1 and
        len(set((x.hand   for x in key))) == 1
    )

def lsb(key: 'list[kb.Position]'):
    return (
        not rlb(key) and
        not sfb(key) and
        key[0].hand == key[1].hand and
        any(abs(x.col) and x.finger == 3 for x in key) and
        any(x.finger == 2 for x in key)
    )

def hsb(key: 'list[kb.Position]'):
    return (
        not rlb(key) and
        not sfb(key) and
        key[0].hand == key[1].hand and
        abs(key[0].row - key[1].row) == 1 and
        max(key, key=lambda x: x.row).finger in [1, 2]
    )

def fsb(key: 'list[kb.Position]'):
    return (
        not rlb(key) and
        not sfb(key) and
        key[0].hand == key[1].hand and
        abs(key[0].row - key[1].row) == 2 and
        max(key, key=lambda x: x.row).finger in [1, 2]
    )

