#!/usr/bin/env python3
from flask import Flask, redirect, url_for, render_template, request, make_response

# from dotenv import dotenv_values
import os
import datetime
import glob
import json
import subprocess
import markdown
import urllib
# from tkinter import filedialog
import subprocess

# config = dotenv_values()  # take environment variables from .env.
cl_length = 7
config = {
    "time": ["00:00"] * cl_length,
    "dirs": [[""] * cl_length for _ in range(7)],
}
if os.path.exists("config.json"):
    with open("config.json", "r") as cf:
        config = json.loads(cf.read())

app = Flask(__name__)


@app.route("/")
@app.route("/<day>/<cl>/")
def root(day=None, cl=None):
    is_root = False
    now = datetime.datetime.now()
    nowday = now.weekday()  # 月=0
    nowcl = 0
    for cltime in config["time"]:
        nowendtime = cltime
        if now.time() < datetime.time(hour=int(cltime[:2]), minute=int(cltime[-2:]), second=0):
            break
        nowcl += 1
    if nowcl >= cl_length:
        nowcl = cl_length - 1
    if cl is None:
        is_root = True
        day = nowday
        cl = nowcl
    else:
        day = int(day)
        cl = int(cl)
    targetdir = getdir(day, cl)
    # targetdir = os.path.join(rootdir, cldir)
    cldir = targetdir[targetdir.rfind("/")+1:]
    files = []
    if os.path.exists(targetdir):
        files = os.listdir(targetdir)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(targetdir, x)))
        files = [f for f in files if f.endswith(".pdf") or f.endswith(".PDF")]
    description_raw = getdescription(day, cl)
    description = markdown.markdown(description_raw)

    return render_template(
        "index.html",
        is_root=is_root,
        day=day,
        cl=cl,
        cl_length=cl_length,
        nowday=nowday,
        nowcl=nowcl,
        nowendtime=nowendtime,
        files=files,
        cldir=cldir,
        description=description,
        description_raw=description_raw,
    )

@app.route("/<day>/<cl>/edit", methods=["post"])
def editsave(day=None, cl=None):
    day = int(day)
    cl = int(cl)
    description_raw = request.form["description"]
    savedescription(day, cl, description_raw)
    return redirect(url_for("root", day=day, cl=cl))

def saveconfig():
    with open("config.json", "w") as cf:
        cf.write(json.dumps(config))

def getdescription(day, cl):
    targetdir = getdir(day, cl)
    # targetdir = os.path.join(rootdir, cldir)
    if os.path.exists(os.path.join(targetdir, "myclass.md")):
        with open(os.path.join(targetdir, "myclass.md"), "r") as fs:
            return fs.read()
    return ""
def savedescription(day, cl, md):
    targetdir = getdir(day, cl)
    # targetdir = os.path.join(rootdir, cldir)
    if os.path.exists(targetdir):
        with open(os.path.join(targetdir, "myclass.md"), "w") as fs:
            fs.write(md)


def getdir(day, cl):
    dirs = ""
    dirs = config["dirs"][day]
    targetdir = ""
    targetdir = dirs[cl]
    return targetdir


@app.route("/<day>/<cl>/open")
def opendir(day, cl):
    day = int(day)
    cl = int(cl)
    target = getdir(day, cl)
    # target = os.path.join(rootdir, cldir)
    if os.path.exists(target):
        try:
            subprocess.Popen(["explorer.exe", target])  # windows
        except:
            try:
                subprocess.Popen(["open", target])  # mac
            except:
                subprocess.Popen(["xdg-open", target])  # linux
    return ""


@app.route("/<day>/<cl>/<filename>")
def getfile(day, cl, filename):
    day = int(day)
    cl = int(cl)
    target = getdir(day, cl)
    # target = os.path.join(rootdir, cldir, filename)
    target = os.path.join(target, filename)
    if os.path.exists(target):
        with open(target, "rb") as f:
            res = make_response(f.read())
            res.headers["content-type"] = "application/pdf"
            return res

@app.route("/config/<day>")
def configpage(day):
    day = int(day)
    return render_template(
        "config.html",
        day=day,
        subtitle="Configuration",
        time=config["time"],
        dir=config["dirs"][day]
    )
@app.route("/config/selectdir/<day>/<cl>")
def config_dir(day, cl):
    day = int(day)
    cl = int(cl)
    dir = subprocess.run(["./dialog.py", config["dirs"][day][cl]], stdout=subprocess.PIPE, encoding="utf-8").stdout
    config["dirs"][day][cl] = dir
    saveconfig()
    return dir

@app.route("/config/settime/<day>/<cl>/<tm>")
def settime(day, cl, tm):
    day = int(day)
    cl = int(cl)
    config["time"][cl] = tm
    saveconfig()
    return ""

if __name__ == "__main__":
    app.run(port=8000)
