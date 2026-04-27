from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String

Base = declarative_base()

class Product(Base):

    # This tells SQLAlchemy: -> Create a table named product in the database
    __tablename__ = "product"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)