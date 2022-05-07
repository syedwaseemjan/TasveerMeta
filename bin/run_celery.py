#! /usr/bin/env python
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR, 'app')))

from app.tasks import app

app.worker_main(
    argv=[
        'worker', '--loglevel=info', '--concurrency=2', '--without-gossip'
    ]
)

if __name__ == '__main__':
    worker = app.Worker(include=['app.tasks'])
    worker.start()
