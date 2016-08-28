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
argp.add_argument("FILE", help="android backup file")

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


''' moov seems to store data in a single row as json blobs.
    queries passed here should select only the json rows, and
    fields are the json keys we are interested in'''
def query_json_csv(sql, q, fields):

    print(",".join(fields))
    for r in sql.execute(q):
        for f in fields:
            for col in r:
                js = json.loads(col)
                if f in js:
                    print("%s," % js[f], end="")
        print()


dbfile = readfile(args.FILE)
if args.sqlite:
    subprocess.run(["/usr/bin/sqlite3", dbfile.name])

if args.csv:
    sql = sqlite3.connect(dbfile.name).cursor()
    query_json_csv(sql,
            "SELECT program_specific_data, local_cache FROM workouts",
            ["lap_count",
             "stroke_count",
             "distance",
             "distance_per_stroke",
             "stroke_rate"])
    sql.close()

