[![Flake8 Actions Status](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/flake8.yaml/badge.svg)](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/flake8.yaml)
[![Black Actions Status](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/black.yaml/badge.svg)](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/black.yaml)
[![Tests Actions Status](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/tests.yaml/badge.svg)](https://github.com/syedwaseemjan/TasveerMeta/actions/workflows/tests.yaml)

# TasveerMeta
TasveerMeta is a distributed python application that downloads images from S3, extracts metadata from each image (only EXIF for now) and stores it to sqlite DB. It employs queues and background workers to achieve this in a distributed fashion. What is EXIF? See [here](http://www.howtogeek.com/203592/what-is-exif-data-and-how-to-remove-it)

## Concept

Boto library is used for handling interaction with S3. After listing all files in the bucket, celery background task is responsible for downloading and processing each individual image. I am using [Pillow](https://pillow.readthedocs.io/en/3.1.x) for extracting the exif information from image. Sqlite DB is used for storing image data. EXIF information is stored as serialized dictionary in DB.

RabbitMq task queue is used with celery for queueing tasks. Celery gives some other options like redis too. Please look at celery docs for that.

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org)
2. [Sqlite](https://sqlite.org)
2. [RabbitMQ](https://www.rabbitmq.com)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone git@github.com:syedwaseemjan/TasveerMeta.git
    $ cd TasveerMeta

#### 2. Create and initialize virtualenv for the project:

    $ virtualenv tasveer_meta
    $ source tasveer_meta/bin/activate
    $ pip install -r requirements/base.txt

#### 3. To run unit tests:

    $ python -m unittest tests.server_test

#### 4. Run the celery background task:
    
    Make sure RabbitMQ server is running and `CELERY_BROKER` is set in app/config.py
    $ python bin/run_celery.py 

#### 5. Run the application:

    $ python bin/run_server.py

    Default bucket is "waldo-recruiting" but you can use any other. Use

    $ python bin/run_server.py <Your-Bucket-Name>


## Best Practices

This project employs automated checkers to make sure that all contributions follow basic conventions.

- [`black`](https://github.com/python/black): to check the code style.
- [`flake8`](https://pypi.org/project/flake8/): to check for PEP-8, McCabe
  complexity, [`isort`](https://pypi.org/project/isort/) violations,
  [pyflakes](https://pypi.org/project/pyflakes/) checks (such as unused
  imports/variables, etc).

Any pull request that violates any of these convention will fail and must
be fixed before asking for a code review.


### Setting up commit hooks

In order to avoid submitting failing PRs, **make sure** to install pre-commit
hooks configured in this repo by running:

```
$ pip install pre-commit
$ pre-commit install
```

Now, every time you try to commit your code `black` will automatically reformat it, `isort` will
automatically sort your imports and `flake8` will look for and report any common issues found on
the code you are trying to commit.


### Helpful Commands

There are a few commands to help you out with the task of keeping your code compliant
with BriteLines standards:

1. Run `black` and `flake8` checkers:

```
$ flake8
```

2. Fix all the code style and import order issues:

```
$ black --check .
```


### References:
1. https://gist.github.com/alwaysunday/db0b32f5ce0538afbb75ccf143adf116
