import os
import json
from itertools import islice
from flask import Flask, request, abort

import classify, kb

app = Flask(__name__)

def param(name: str):
    for keys in request.args.getlist(name):
        for x in keys:
            yield x

def filters(name: str):
    for keys in request.args.getlist(name):
        dir, val = keys.split(':')

        if dir == 'lt':
            yield lambda x: x < float(val)
        if dir == 'gt':
            yield lambda x: x > float(val)

@app.route('/layout/<name>')
def layout(name: str):
    path = f'layouts/{name}.json'

    if not os.path.exists(path):
        abort(404)

    with open(path, 'r') as f:
        data = json.load(f)

    return data

@app.route('/layouts')
def layouts():
    limit = request.args.get('limit', default=50, type=int)
    page = request.args.get('page', default=1, type=int)

    sort = request.args.get('sort')
    order = request.args.get('order', default='asc')

    layouts = (
        x for x in kb.layouts()
        if all(x.key[y].finger == 0 for y in param('pinky'))
        if all(x.key[y].finger == 1 for y in param('ring'))
        if all(x.key[y].finger == 2 for y in param('middle'))
        if all(x.key[y].finger == 3 for y in param('index'))
        if all(x.key[y].finger == 4 for y in param('thumb'))
        if all(x.key[y].hand   == 0 for y in param('left'))
        if all(x.key[y].hand   == 1 for y in param('right'))
        if all(x.key[y].row   == 0 for y in param('home'))
        if all(x.key[y].col   == 0 for y in param('home'))
        if all(classify.sfb(x.pos(y)) for y in request.args.getlist('any'))
        if all(func(x.metric('sfb')) for func in filters('sfb'))
        if all(func(x.metric('lsb')) for func in filters('lsb'))
        if all(func(x.metric('hsb')) for func in filters('hsb'))
        if all(func(x.metric('fsb')) for func in filters('fsb'))
    )

    if sort:
        layouts = sorted(layouts, key=lambda x: x.metric(sort), reverse=(order=='desc'))

    layouts = islice(layouts, limit * (page - 1), limit * page)

    return [x.name for x in layouts]

if __name__ == '__main__':
    app.run()