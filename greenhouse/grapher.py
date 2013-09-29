import sqlite3
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot

con = sqlite3.connect('tempseries')
con.text_factory = str
cur = con.cursor()
cur.execute("select value from temp_series where event = 'Temperature' ORDER by date ASC")
temp = [r[0] for r in cur.fetchall()]
cur.execute("select value from temp_series where event = 'Light intensity' ORDER by date ASC")
light = [s[0] for s in cur.fetchall()]
# Temperature plot - Translated and scaled to realistic outdoor termperatures
pyplot.subplot(211)
pyplot.plot(temp)
x1,x2,y1,y2 = pyplot.axis()
print(x1,x2,y1,y2)
pyplot.axis([x1,x2,-20.0,40.0])
pyplot.grid(True)
pyplot.axhline(y=0, linestyle='--')
pyplot.ylabel('Temperature')
pyplot.xlabel('Sample')
# Light Intensity plot - Runs from 0 to maany
pyplot.subplot(212)
pyplot.plot(light)
x1,x2,y1,y2 = pyplot.axis()
pyplot.axis([x1,x2, 0, y2])
pyplot.grid(True)
pyplot.ylabel('Light Intensity')
pyplot.xlabel('Sample')
pyplot.savefig('simple.png')
pyplot.show()
