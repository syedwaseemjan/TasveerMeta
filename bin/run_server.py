#! /usr/bin/env python

from __future__ import absolute_import

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.abspath(os.path.join(PROJECT_DIR, 'app')))

if __name__ == "__main__":
    from app.main import Main

    aws_bucket_name = None
    if len(sys.argv) > 1:
        aws_bucket_name = sys.argv[1]
    Main().load_images(aws_bucket_name)
