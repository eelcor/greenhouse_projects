from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger_base import Item, Average, Base
import time, weather, datetime
from dateutil import parser

engine = create_engine('sqlite:///logbase.db')
Base.metadata.bind = engine
weer = weather.weather()

DBSession = sessionmaker(bind=engine)
session = DBSession()

while 1:
	print datetime.time()
	a = weer.measure()
	dt = parser.parse(a['time'])
	light = Item(name='light', value=a['light'], timestamp=dt)
	pressure = Item(name='pressure', value=a['pressure'], timestamp=dt)
	temp = Item(name='temp', value=a['temp'], timestamp=dt)
	session.add(light)
	session.add(pressure)
	session.add(temp)
	session.commit()
	time.sleep(60)
	


