
import logging
from app.tasks import process_image, get_s3_bucket
from models import Image
from exceptions import UniqueValuesException

logger = logging.getLogger()


class Main(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        handler = logging.FileHandler('server.log')
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '[%(asctime)s: %(levelname)s/%(name)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def load_images(self, bucket_name=None):
        bucket = get_s3_bucket(bucket_name)
        if bucket:
            for key in bucket.objects.all():
                image_name = key.key
                if not image_name.endswith(".tar.gz") and not image_name.endswith("undefined.jpg"):
                    image = Image(name=image_name, size=key.size)
                    try:
                        image.save()
                    except UniqueValuesException as exe:
                        logger.info(exe)
                    else:
                        process_image.delay(image.id, image.name)
