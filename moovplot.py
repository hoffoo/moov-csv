#!/usr/bin/env python
import zlib
import sys
import io
import tarfile
import sqlite3
import tempfile
import json
import argparse

''' reads file at arg and returns a sqlite db connection '''
def readfile(path):

    f = open(path, "r+b")
    f.seek(24)

    buf = io.BytesIO(zlib.decompress(f.read()))
    tar = tarfile.open(0, "r", buf)

    tmpf = tempfile.NamedTemporaryFile()
    dbtar = None
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

    return sqlite3.connect(tmpf.name).cursor()

def query_csv(q, fields):
    for f in fields:
        print("%s," % f, end="")
    print()
    for r in c.execute(q):
        for f in fields:
            print("%s," % str(json.loads(r[0])[f]), end="")
        print()



c = readfile(sys.argv[1])
query_csv("SELECT program_specific_data AS user_data FROM workouts",  ["lap_count", "stroke_count"])

c.close()
