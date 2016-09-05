#!/usr/bin/env python
import zlib
import sys
import io
import tarfile
import sqlite3
import tempfile
import json
import argparse
import subprocess

argp = argparse.ArgumentParser(description="moov csv and plot")
argp.add_argument("--csv",    action="store_true", help="output to csv")
argp.add_argument("--sqlite", action="store_true", help="launch sqlite shell for exploring")
argp.add_argument("-b", action="store_true", help="generate a backup to use")
argp.add_argument("FILE", nargs="?", default="", help="android backup file")

args = argp.parse_args()
#sys.exit(1)

''' reads android archive and returns a tempfile of the sqlite db'''
def readfile(path):

    f = open(path, "r+b")
    # im not sure why skip the first 24 bytes
    # something about how android zips the tarball
    f.seek(24)

    #unzip
    buf = io.BytesIO(zlib.decompress(f.read()))
    tar = tarfile.open(0, "r", buf)

    # extract sqlite databases from archive
    dbtar = None
    tmpf = tempfile.NamedTemporaryFile()
    for member in tar.getmembers():
        if not member.name.startswith("apps/cc.moov.one/"):
            continue
        if member.name.endswith("user.db"):
            dbtar = tar.extractfile(member)
            tmpf.write(dbtar.read())
            dbtar.close()
            break

    if dbtar == None:
        raise Exception("failed finding user.db in archive")

    f.close()
    buf.close()
    tar.close()
    tmpf.flush()

    return tmpf


''' moov seems to store data some data in json blobs we attempt to decode into
json if we see a str and select the fields. otherwise we simply print the field'''
def query(sql, q, fields):

    sql.execute(q)
    print(",".join(fields))
    for r in sql.fetchall():
        for col in r:
            for f in fields:
                # first try to get the field from json
                if type(col) == str:
                    js = json.loads(col)
                    if f in js:
                        print("%s," % js[f], end="")
                    continue

                # failed to get this col from json, try from the row
                try:
                    print("%s," % r[f], end="")
                except IndexError:
                    pass
        print()

if args.FILE == "" and not args.b:
    argp.error("either specify a backup file or the -b option")

bkfile = args.FILE
if args.b:
    tmpf = tempfile.NamedTemporaryFile()
    subprocess.run(["adb", "backup", "-f", tmpf.name, "-noapk", "cc.moov.one"])
    bkfile = tmpf.name

dbfile = readfile(bkfile)
if args.sqlite:
    subprocess.run(["/usr/bin/sqlite3", dbfile.name])

if args.csv:
    conn = sqlite3.connect(dbfile.name)
    conn.row_factory = sqlite3.Row
    sql = conn.cursor()
    print("\n\nswims:")
    query(sql,
            "SELECT duration,program_specific_data, local_cache FROM workouts WHERE workout_type = 2",
            ["duration",
             "lap_count",
             "stroke_count",
             "distance",
             "distance_per_stroke",
             "stroke_rate"])
    print("\n\nruns:")
    query(sql,
            "SELECT duration,local_cache FROM workouts WHERE workout_type = 0",
            ["duration",
             "average_cadence",
             "average_speed",
             "distance"])
    sql.close()

