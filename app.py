#!/usr/bin/env python3
from flask import Flask, redirect, url_for, render_template, make_response
from dotenv import dotenv_values
import os
import datetime

config = dotenv_values()  # take environment variables from .env.
rootdir = config["ROOTDIR"]

app = Flask(__name__)

@app.route("/")
def root():
    now = datetime.datetime.now()
    day = now.weekday() #月=0
    cl = 0
    for cltime in config["TIME"].split():
        if now.time() < datetime.time(hour=int(cltime[:2]), minute=int(cltime[-2:]), second=0):
            break
        cl += 1
    targetdir = getdir(day, cl)
    files = []
    if targetdir:
        files = os.listdir(targetdir)
        files = [f for f in files if f.endswith(".pdf") or f.endswith(".PDF")]
        return render_template("index.html", day=day, cl=cl, files=files, targetdir=targetdir)

def getdir(day, cl):
    dirs = ""
    if f"DIR{day}" in config:
        dirs = config[f"DIR{day}"].split(":")
    targetdir = ""
    if cl >= 0 and cl < len(dirs):
        targetdir = os.path.join(rootdir, dirs[cl])
    return targetdir

@app.route("/<day>/<cl>/<filename>")
def getfile(day, cl, filename):
    day = int(day)
    cl = int(cl)
    target = os.path.join(getdir(day, cl), filename)
    if os.path.exists(target):
        with open(target, "rb") as f:
            res = make_response(f.read())
            res.headers["content-type"] = "application/pdf"
            return res
