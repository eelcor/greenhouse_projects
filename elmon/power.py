from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:////home//pi//notebooks//power.db', echo=True)
Base = declarative_base()

class Power(Base):
	__tablename__ = "powervalues"
	
	id = Column(Integer, primary_key=True)
	counter = Column(Integer)
	timestamp = Column(DateTime)
	power = Column(Float)
	kwh = Column(Float)

	def __init__(self, timestamp, counter, power, kwh):
		self.timestamp = timestamp
		self.counter = counter
		self.power = power
		self.kwh = kwh
 
# create tables
Base.metadata.create_all(engine)
