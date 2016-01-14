from __future__ import unicode_literals
from celery.result import ResultSet
from tasks import find_prime
from bottle import route, run
import json


CHUNK_SIZE = 1000


def is_prime(numbers):
    return find_prime.delay(numbers)


@route('/check_prime/<minimum>/<maximum>')
def get_check_prime(minimum, maximum):
    data = range(int(minimum), int(maximum))
    chunks = [data[x:x+CHUNK_SIZE] for x in xrange(0, len(data), CHUNK_SIZE)]
    results = ResultSet(map(is_prime, chunks))
    result = sum(results.get(), [])
    return json.dumps([x[0] for x in result if x[1]])

run(host='0.0.0.0', port=8080, debug=True)
