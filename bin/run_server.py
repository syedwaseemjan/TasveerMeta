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

if __name__ == "__main__":
    from app.main import Main

    aws_bucket_name = None
    if len(sys.argv) > 1:
        aws_bucket_name = sys.argv[1]
    Main().load_images(aws_bucket_name)
