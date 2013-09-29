import sqlite3
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

#Connect to the current database and retrieve the time series
con = sqlite3.connect('tempseries')
con.text_factory = str
cur = con.cursor()
cur.execute("select value from temp_series where event = 'Temperature' ORDER by date ASC")
temp = [r[0] for r in cur.fetchall()]
cur.execute("select value from temp_series where event = 'Light intensity' ORDER by date ASC")
light = [s[0] for s in cur.fetchall()]
cur.execute("select value from temp_series where event = 'Pressure' ORDER by date ASC")
pressure = [t[0] for t in cur.fetchall()]

#Plot the temperature
pyplot.subplot(311)
pyplot.plot(temp)
x1,x2,y1,y2 = pyplot.axis()
print(x1,x2,y1,y2)
pyplot.axis([x1,x2,-20.0,40.0])
pyplot.grid(True)
pyplot.axhline(y=0, linestyle='--')
pyplot.ylabel('Temperature')
pyplot.xlabel('Sample')

#Plot the light intensity
pyplot.subplot(312)
pyplot.plot(light)
pyplot.grid(True)
pyplot.ylabel('Light Intensity')
pyplot.xlabel('Sample')

#Plot the pressure
pyplot.subplot(313)
pyplot.plot(pressure)
pyplot.grid(True)
pyplot.ylabel('Pressure')
pyplot.xlabel('Sample')

#Wrap it up
pyplot.savefig('simple.png')
pyplot.show()
