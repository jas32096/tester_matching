from flask import Flask, make_response, request, jsonify

from user_search import *
from user_search.cli.cli import search, _parse

import io

app = Flask(__name__)


FORMATS = {'json', 'tsv'}

@app.route('/search')
def test():
    args = (request.args.get('c', 'ALL'), request.args.get('d', 'ALL'))
    fmt = request.args.get('fmt', 'json').lower()

    if fmt not in FORMATS:
        return jsonify({'error': f'{fmt} is not one of {FORMATS}'}), 400

    text = io.StringIO()
    search(**_parse(args), fmt=fmt, file=text)
    
    resp = make_response(text.getvalue())
    resp.headers['Content-Type'] = 'application/json' if fmt == 'json' else 'text/tab-separated-values'
    return resp
