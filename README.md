# TasveerMeta
TasveerMeta is a python application that downloads images from S3, extracts metadata from each image (only EXIF for now) and stores it to sqlite DB. What is EXIF? See [here](http://www.howtogeek.com/203592/what-is-exif-data-and-how-to-remove-it)

## Concept

Boto library is used for handling interaction with S3. After listing all files in the bucket, celery background task is responsible for downloading and processing each individual image. I am using [Pillow](https://pillow.readthedocs.io/en/3.1.x) for extracting the exif information from image. Sqlite DB is used for storing image data. EXIF information is stored as serialized dictionary in DB.

RabbitMq task queue is used with celery for queueing tasks. Celery gives some other options like redis too. Please look at celery docs for that.

Due to shortage of time 
No tests, No logging (Just print), No detailed exception handling

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

    I am using Pillow for extracting exif information from images. If you find any issue during its installation try upgrading your pip. (That worked for me atleast)
    $ pip install --upgrade pip

#### 3. To run unit tests:

    $ python -m unittest tests.server_test

#### 4. Run the celery background task:

    $ python bin/run_celery.py 

#### 5. Run the application:

    $ python bin/run_server.py

    Default bucket is "waldo-recruiting" but you can use any other. Use

    $ python bin/run_server.py <Your-Bucket-Name>

### References:
1. https://gist.github.com/alwaysunday/db0b32f5ce0538afbb75ccf143adf116
