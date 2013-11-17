import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData

Base = declarative_base()

class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)
	name = Column(String(250))
	value = Column(Float)

class Average(Base):
	__tablename__ = 'average'
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)
	name = Column(String(250))
	value = Column(Float)

engine = create_engine('sqlite:///logbase.db')
Base.metadata.create_all(engine)
