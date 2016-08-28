#!/usr/bin/env python
import zlib
import sys
import StringIO
import tarfile
import sqlite3
import tempfile
import json
import matplotlib.pyplot as plt

def readfile(path):

    f = open(path, "r")
    f.seek(24)

    buf = StringIO.StringIO(zlib.decompress(f.read()))
    tar = tarfile.open(0, "r", buf)

    db = StringIO.StringIO()
    for member in tar.getmembers():
        if not member.name.startswith("apps/cc.moov.one/"):
            continue
        if member.name.endswith("user.db"):
            dbtar = tar.extractfile(member)
            db.write(dbtar.read())
            db.seek(0)
            dbtar.close()
            break


    if dbtar == None:
        raise Exception("failed finding user.db in archive")

    f.close()
    buf.close()
    tar.close()

    return db

def opensqlite(f):

    tmpf = tempfile.NamedTemporaryFile()
    tmpf.write(f.read())

    f.close()
    return sqlite3.connect(tmpf.name)

def query_csv(cursor, q, fields):
    for f in fields:
        sys.stdout.write(f + ",")
    print
    for r in c.execute(q):
        for f in fields:
            sys.stdout.write(str(json.loads(r[0])[f]) + ",")
        print



db = readfile(sys.argv[1])

conn = opensqlite(db)
c = conn.cursor()
query_csv(c, "select program_specific_data from workouts",  ["lap_count", "stroke_count"])

c.close()
