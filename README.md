# Moov

I like my Moov fitness tracker but it does a shit job at visualizing swim
data over time. So far there is no way to export.

This script uses an android backup of the moov app to extract the sqlite
database and run queries against it. It outputs CSV, you can then import that
data into whatever app you wish and plot away.

It prints run and swim data. It will probably work for other workout modes, 
let me know if you are interested and ill add.

### Prereq

1. Android - (doesn't need to be rooted) the process could be similar for IOS
   but I have not way to test

### Features
```
usage: moovplot.py [-h] [--csv] [--sqlite] FILE

moov csv and plot

positional arguments:
  FILE        android backup file

optional arguments:
  -h, --help  show this help message and exit
  --csv       output to csv
  --sqlite    launch sqlite shell for exploring
```

```
$ ./moovplot.py --csv /tmp/bk 


swims:
duration,lap_count,stroke_count,distance,distance_per_stroke,stroke_rate
2447,85,846,1787.6519775390625,2.1130638122558594,2.330496311187744,
2420,90,879,1892.8079833984375,2.153365135192871,2.3392841815948486,
2818,95,880,1997.9639892578125,2.270413637161255,2.440192937850952,


runs:
duration,average_cadence,average_speed,distance
1679,158.55850219726562,3.008333444595337,5054,
1736,157.34739685058594,3.055588483810425,5170,
```

### Getting the Data

Android:

1. install the android sdk (only the cli tools are required) https://developer.android.com/sdk/index.html
1. enable dev access on your phone
1. enable usb debugging
1. create a backup and authorize on the phone

```
# create a backup of the moov app at /tmp/bk
adb backup -f /tmp/bk -noapk cc.moov.one

# run
moovplot.py /tmp/bk
```
