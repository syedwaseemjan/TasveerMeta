#! /usr/bin/env python
import os
import sys

thisdir = os.path.dirname(__file__)
app_root_dir = os.path.abspath(os.path.join(thisdir, '..'))
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

app_dir = os.path.abspath(os.path.join(thisdir, '../app'))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from app.tasks import app

app.worker_main(
    argv=[
        'worker', '--loglevel=info', '--concurrency=2', '--without-gossip'
    ]
)

if __name__ == '__main__':
    worker = app.Worker(include=['app.tasks'])
    worker.start()
