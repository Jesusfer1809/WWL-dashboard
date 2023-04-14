import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os


lectures = [{"pressure":"52.026269","time":"Thu, 23 Feb 2023 02:00:00 "},
{"pressure":"52.026260","time":"Thu, 23 Feb 2023 06:00:00 "},
{"pressure":"52.026274","time":"Thu, 23 Feb 2023 10:00:00 "},
{"pressure":"52.216681","time":"Thu, 23 Feb 2023 18:00:00 "},
{"pressure":"52.026262","time":"Fri, 24 Feb 2023 02:00:00 "},
{"pressure":"52.026280","time":"Fri, 24 Feb 2023 06:00:00 "},
{"pressure":"52.216685","time":"Fri, 24 Feb 2023 10:00:00 "},
{"pressure":"52.026298","time":"Fri, 24 Feb 2023 14:00:00 "},
{"pressure":"52.026295","time":"Fri, 24 Feb 2023 18:00:00 "},
{"pressure":"51.837444","time":"Fri, 24 Feb 2023 22:00:00 "},
{"pressure":"51.837436","time":"Sat, 25 Feb 2023 02:00:00 "},
{"pressure":"52.026266","time":"Sat, 25 Feb 2023 06:00:00 "},
{"pressure":"52.026286","time":"Sat, 25 Feb 2023 10:00:00 "},
{"pressure":"52.216692","time":"Sat, 25 Feb 2023 14:00:00 "},
{"pressure":"51.837461","time":"Sat, 25 Feb 2023 18:00:00 "},
{"pressure":"52.026275","time":"Sat, 25 Feb 2023 22:00:00 "},
{"pressure":"51.837444","time":"Sun, 26 Feb 2023 02:00:00 "},
{"pressure":"51.837468","time":"Sun, 26 Feb 2023 06:00:00 "},
{"pressure":"52.026259","time":"Sun, 26 Feb 2023 10:00:00 "},
{"pressure":"52.026298","time":"Sun, 26 Feb 2023 14:00:00 "},
{"pressure":"51.837466","time":"Sun, 26 Feb 2023 18:00:00 "},
{"pressure":"52.026252","time":"Sun, 26 Feb 2023 22:00:00 "},
{"pressure":"51.837448","time":"Mon, 27 Feb 2023 06:00:00 "},
{"pressure":"52.026276","time":"Mon, 27 Feb 2023 14:00:00 "},
{"pressure":"52.216654","time":"Mon, 27 Feb 2023 22:00:00 "},
{"pressure":"52.216643","time":"Tue, 28 Feb 2023 02:00:00 "},
{"pressure":"52.216645","time":"Tue, 28 Feb 2023 10:00:00 "},
{"pressure":"52.026275","time":"Tue, 28 Feb 2023 14:00:00 "},
{"pressure":"52.026256","time":"Wed, 01 Mar 2023 02:00:00 "},
{"pressure":"52.026257","time":"Wed, 01 Mar 2023 14:00:00 "},
{"pressure":"52.216657","time":"Wed, 01 Mar 2023 18:00:00 "},
{"pressure":"52.216651","time":"Wed, 01 Mar 2023 22:00:00 "},
{"pressure":"52.216649","time":"Thu, 02 Mar 2023 06:00:00 "},
{"pressure":"52.026249","time":"Thu, 02 Mar 2023 10:00:00 "},
{"pressure":"52.216658","time":"Thu, 02 Mar 2023 14:00:00 "},
{"pressure":"52.026270","time":"Thu, 02 Mar 2023 18:00:00 "},
{"pressure":"52.026245","time":"Thu, 02 Mar 2023 22:00:00 "},
{"pressure":"51.837430","time":"Fri, 03 Mar 2023 02:00:00 "},
{"pressure":"52.026262","time":"Fri, 03 Mar 2023 06:00:00 "},
{"pressure":"52.026237","time":"Fri, 03 Mar 2023 22:00:00 "},
{"pressure":"52.026254","time":"Sat, 04 Mar 2023 02:00:00 "},
{"pressure":"51.837441","time":"Sat, 04 Mar 2023 10:00:00 "},
{"pressure":"52.026262","time":"Sat, 04 Mar 2023 14:00:00 "},
{"pressure":"51.648624","time":"Sat, 04 Mar 2023 18:00:00 "},
{"pressure":"51.837435","time":"Sun, 05 Mar 2023 02:00:00 "},
{"pressure":"51.837422","time":"Sun, 05 Mar 2023 06:00:00 "},
{"pressure":"51.837435","time":"Sun, 05 Mar 2023 10:00:00 "},
{"pressure":"52.026271","time":"Sun, 05 Mar 2023 14:00:00 "},
{"pressure":"51.837440","time":"Sun, 05 Mar 2023 18:00:00 "},
{"pressure":"52.026232","time":"Sun, 05 Mar 2023 22:00:00 "},
{"pressure":"52.026252","time":"Mon, 06 Mar 2023 02:00:00 "},
{"pressure":"51.837442","time":"Mon, 06 Mar 2023 06:00:00 "},
{"pressure":"52.026252","time":"Mon, 06 Mar 2023 10:00:00 "},
{"pressure":"51.837466","time":"Mon, 06 Mar 2023 14:00:00 "},
{"pressure":"51.648643","time":"Mon, 06 Mar 2023 18:00:00 "},
{"pressure":"51.648622","time":"Mon, 06 Mar 2023 22:00:00 "},
{"pressure":"51.459800","time":"Tue, 07 Mar 2023 06:00:00 "},
{"pressure":"51.459800","time":"Tue, 07 Mar 2023 10:00:00 "},
{"pressure":"51.459794","time":"Tue, 07 Mar 2023 18:00:00 "},
{"pressure":"51.837446","time":"Tue, 07 Mar 2023 22:00:00 "},
{"pressure":"51.837439","time":"Wed, 08 Mar 2023 02:00:00 "},
{"pressure":"51.459782","time":"Wed, 08 Mar 2023 06:00:00 "},
{"pressure":"51.837446","time":"Wed, 08 Mar 2023 10:00:00 "},
{"pressure":"51.648629","time":"Wed, 08 Mar 2023 14:00:00 "},
{"pressure":"51.648630","time":"Wed, 08 Mar 2023 18:00:00 "},
{"pressure":"51.837435","time":"Wed, 08 Mar 2023 22:00:00 "},
{"pressure":"51.837423","time":"Thu, 09 Mar 2023 02:00:00 "},
{"pressure":"52.026253","time":"Thu, 09 Mar 2023 06:00:00 "},
{"pressure":"51.837443","time":"Thu, 09 Mar 2023 10:00:00 "},
{"pressure":"51.837453","time":"Thu, 09 Mar 2023 14:00:00 "}]


def getPressure(obj):
    return float(obj['pressure'])

def getDate(obj):
    
    return obj['time']

pressure = list(map(getPressure, lectures))
dates = list(map(getDate, lectures))

print(pressure)

# Data for plotting
t = dates
s = pressure

plt.plot(t,s)

plt.xlabel('Dates')
plt.ylabel('Pressure (KPa)')
plt.xticks(visible=False)
plt.fill_between(t, s, min(pressure), color=['#477C9A'], alpha=.1)

plt.grid()

plt.savefig(os.getcwd() + "/public/test.png")



plt.show()

["2023-02-22 21:00:00", "2023-02-23 01:00:00", "2023-02-23 05:00:00", "2023-02-23 09:00:00", "2023-02-23 13:00:00", "2023-02-23 17:00:00", "2023-02-23 21:00:00", "2023-02-24 05:00:00", "2023-02-24 09:00:00", "2023-02-24 13:00:00", "2023-02-24 17:00:00", "2023-02-25 01:00:00", "2023-02-25 05:00:00", "2023-02-25 09:00:00", "2023-02-25 13:00:00", "2023-02-25 17:00:00", "2023-02-25 21:00:00", "2023-02-26 01:00:00", "2023-02-26 05:00:00", "2023-02-26 09:00:00", "2023-02-26 13:00:00", "2023-02-26 17:00:00", "2023-02-27 01:00:00", "2023-02-27 09:00:00", "2023-02-27 17:00:00", "2023-02-27 21:00:00", "2023-02-28 05:00:00", "2023-02-28 09:00:00", "2023-02-28 13:00:00", "2023-02-28 21:00:00", "2023-03-01 09:00:00", "2023-03-01 13:00:00", "2023-03-01 17:00:00", "2023-03-01 21:00:00", "2023-03-02 01:00:00", "2023-03-02 05:00:00", "2023-03-02 09:00:00", "2023-03-02 13:00:00", "2023-03-02 17:00:00", "2023-03-02 21:00:00", "2023-03-03 01:00:00", "2023-03-03 09:00:00", "2023-03-03 17:00:00", "2023-03-03 21:00:00", "2023-03-04 05:00:00", "2023-03-04 09:00:00", "2023-03-04 21:00:00", "2023-03-05 05:00:00", "2023-03-05 09:00:00", "2023-03-05 13:00:00", "2023-03-05 17:00:00", "2023-03-05 21:00:00", "2023-03-06 01:00:00", "2023-03-06 05:00:00", "2023-03-06 13:00:00", "2023-03-06 17:00:00", "2023-03-07 01:00:00", "2023-03-07 05:00:00", "2023-03-07 13:00:00", "2023-03-07 17:00:00", "2023-03-07 21:00:00", "2023-03-08 01:00:00", "2023-03-08 05:00:00", "2023-03-08 09:00:00", "2023-03-08 13:00:00", "2023-03-08 17:00:00", "2023-03-08 21:00:00", "2023-03-09 05:00:00", "2023-03-09 09:00:00", "2023-03-09 17:00:00", "2023-03-09 21:00:00", "2023-03-10 01:00:00", "2023-03-10 05:00:00"]