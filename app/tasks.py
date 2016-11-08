import json

import boto3
import botocore
from io import BytesIO
from tqdm import tqdm
from botocore.handlers import disable_signing
from celery import Celery
from celery.utils.log import get_task_logger
from PIL import Image as PILImage

from models import dal, Image
from config import CELERY_BROKER, DEFAULT_BUCKET

logger = get_task_logger(__name__)
app = Celery('tasks', broker=CELERY_BROKER)


@app.task
def process_image(image_id, file_name):
    logger.info(f"Processing file. Image ID: {image_id}, Name: {file_name}")

    s3_object = s3.Object(DEFAULT_BUCKET, file_name)
    total_size = float(s3_object.get()['ContentLength'])
    logger.info(f"total_size: {total_size}")
    pbar = tqdm(total=total_size, unit='B',
                unit_scale=True, unit_divisor=1024)

    def progress(bytes_amount):
        pbar.update(bytes_amount)

    bytes_image = BytesIO()
    s3_object.download_fileobj(bytes_image, Callback=progress)
    pbar.close()
    logger.info(f'Download Complete. File: {file_name}. Total Size: {total_size}.')

    exif = json.dumps(read_exif(bytes_image))

    logger.info(f"Extracted exif. Now saving to DB. File: {file_name}")

    image = dal.session.query(Image).get(image_id)
    try:
        image.update(exif_info=exif)
    except AttributeError as exe:
        logger.exception(f"Image: {image_id} does not exist. Error: {exe}")
    else:
        logger.info(f"Exif successfully saved in DB for the image: {image.id}")


def read_exif(file):
    img = PILImage.open(file)
    exif_data = img._getexif()
    return str(exif_data)


def get_s3_bucket(bucket_name):
    s3 = get_s3_connection()
    bucket_name = bucket_name or DEFAULT_BUCKET
    bucket = False
    try:
        bucket = s3.Bucket(bucket_name)
    except botocore.exceptions.ClientError as e:
        logger.exception(e)
    return bucket


def get_s3_connection():
    s3 = boto3.resource('s3')
    s3.meta.client.meta.events.register(
        'choose-signer.s3.*', disable_signing)
    # s3 = boto3.client('s3')
    return s3


s3 = get_s3_connection()
