from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Request(Base):
    __tablename__ = "Requests"
    request_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    status = Column(String(20), default="Pending")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Product(Base):
    __tablename__ = "Products"
    product_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    request_id = Column(UNIQUEIDENTIFIER, ForeignKey("Requests.request_id"))
    product_name = Column(String(255), nullable=False)

class Image(Base):
    __tablename__ = "Images"
    image_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    product_id = Column(UNIQUEIDENTIFIER, ForeignKey("Products.product_id"))
    input_image_url = Column(Text, nullable=False)
    output_image_url = Column(Text, nullable=True)
    status = Column(String(20), default="Processing")
