import os
from uuid import uuid4
import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import DB_URI, SQLALCHEMY_ECHO
from sqlalchemy.exc import IntegrityError
from exceptions import UniqueValuesException

logger = logging.getLogger()
Base = declarative_base()


class Common(object):
    def update(self, *arg, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def save(self):
        dal.session.add(self)
        try:
            dal.session.commit()
            logger.info(f"Successfully saved to DB: {self.name}")
        except IntegrityError as exe:
            dal.session.rollback()
            logger.error(exe.args)
            raise UniqueValuesException(f"Image with name: {self.name} already exists")


class Image(Base, Common):

    __tablename__ = "images"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True, nullable=False)
    size = Column(Integer, nullable=False)
    exif_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"<Image (name='{self.name}', size='{self.size}', exif_info={self.exif_info}, created_at={str_created_at})>"


class DataAccessLayer(object):
    session = None
    engine = None
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", DB_URI))
    conn_string = "sqlite:///{}".format(db_path)

    def __init__(self, conn_string=None):
        logger.info(conn_string)
        self.engine = create_engine(
            conn_string or self.conn_string, echo=SQLALCHEMY_ECHO
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)


dal = DataAccessLayer()
