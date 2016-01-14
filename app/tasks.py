from __future__ import unicode_literals
from celery import Celery


app = Celery('tasks', backend='redis://redis', broker='amqp://guest@rabbit//')


@app.task
def check_prime(number):
    if number % 2 == 0:
        return number, False
    for i in xrange(2, number / 2):
        if number % i == 0:
            return number, False
    return number, True


@app.task
def find_prime(numbers):
    return map(check_prime, numbers)
