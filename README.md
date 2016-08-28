Moov
====

I like my Moov fitness tracker but it does a shit job at visualizing swim
data over time. So far there is no way to export.

This script uses an android backup of the moov app to extract the sqlite
database and run queries against it. It outputs CSV, you can then import that
data into whatever app you wish and plot away.

Presumably it would work for the other workout modes but I don't use them. If
you are interested in another one let me know and I will work on it.

Prereq
====

1. Android - (doesn't need to be rooted) the process could be similar for IOS
   but I have not way to test

Getting the Data
====

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
