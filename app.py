#!/usr/bin/env python3
from flask import Flask, redirect, url_for, render_template, make_response
from dotenv import dotenv_values
import os
import datetime
import glob

config = dotenv_values()  # take environment variables from .env.
rootdir = config["ROOTDIR"]

app = Flask(__name__)

@app.route("/")
@app.route("/<day>/<cl>")
def root(day=None, cl=None):
    if cl is None:
        now = datetime.datetime.now()
        day = now.weekday() #月=0
        cl = 0
        for cltime in config["TIME"].split():
            if now.time() < datetime.time(hour=int(cltime[:2]), minute=int(cltime[-2:]), second=0):
                break
            cl += 1
    else:
        day = int(day)
        cl = int(cl)
    cl_length = len(config["TIME"].split())
    cldir = getdir(day, cl)
    targetdir = os.path.join(rootdir, cldir)
    files = []
    if cldir and os.path.exists(targetdir):
        files = os.listdir(targetdir)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(targetdir, x)))
        files = [f for f in files if f.endswith(".pdf") or f.endswith(".PDF")]
    return render_template("index.html", day=day, cl=cl, cl_length=cl_length, files=files, cldir=cldir)

def getdir(day, cl):
    dirs = ""
    if f"DIR{day}" in config:
        dirs = config[f"DIR{day}"].split(":")
    targetdir = ""
    if cl >= 0 and cl < len(dirs):
        targetdir = dirs[cl]
        return targetdir
    return ""

@app.route("/<day>/<cl>/<filename>")
def getfile(day, cl, filename):
    day = int(day)
    cl = int(cl)
    cldir = getdir(day, cl)
    target = os.path.join(rootdir, cldir, filename)
    if cldir and os.path.exists(target):
        with open(target, "rb") as f:
            res = make_response(f.read())
            res.headers["content-type"] = "application/pdf"
            return res
