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

# config = dotenv_values()  # take environment variables from .env.
config = {
	"rootdir":"",
	"time":[],
	"dirs":[
		[],
		[],
		[],
		[],
		[],
		[],
		[],
	],
	"descriptions":[
		[],
		[],
		[],
		[],
		[],
		[],
		[],
	]
}
if os.path.exists("config.json"):
    with open("config.json", "r") as cf:
        config = json.loads(cf.read())
rootdir = config["rootdir"]

app = Flask(__name__)

@app.route("/")
@app.route("/<day>/<cl>/")
def root(day=None, cl=None):
    is_root = False
    now = datetime.datetime.now()
    nowday = now.weekday() #月=0
    nowcl = 0
    for cltime in config["time"]:
        nowendtime = cltime
        if now.time() < datetime.time(hour=int(cltime[:2]), minute=int(cltime[-2:]), second=0):
            break
        nowcl += 1
    if cl is None:
        is_root = True
        day = nowday
        cl = nowcl
    else:
        day = int(day)
        cl = int(cl)
    cl_length = len(config["time"])
    cldir = getdir(day, cl)
    targetdir = os.path.join(rootdir, cldir)
    files = []
    if cldir and os.path.exists(targetdir):
        files = os.listdir(targetdir)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(targetdir, x)))
        files = [f for f in files if f.endswith(".pdf") or f.endswith(".PDF")]
    description_raw = getdescription(day, cl)
    description = markdown.markdown(description_raw)

    return render_template("index.html",
        is_root=is_root, day=day, cl=cl, nowday=nowday, nowcl=nowcl, cl_length=cl_length, files=files, nowendtime=nowendtime,
        cldir=cldir, description=description, description_raw=description_raw)

# @app.route("/<day>/<cl>/edit")
# def editpage(day=None, cl=None):
#     day = int(day)
#     cl = int(cl)
#     cl_length = len(config["time"])
#     cldir = getdir(day, cl)
#     description_raw = getdescription(day, cl)
#
#     return render_template("edit.html", day=day, cl=cl, cl_length=cl_length, cldir=cldir, description_raw=description_raw)

@app.route("/<day>/<cl>/edit", methods=["post"])
def editsave(day=None, cl=None):
    day = int(day)
    cl = int(cl)
    description_raw = request.form["description"]
    while day >= len(config["description"]):
        config["description"].append([])
    while cl >= len(config["description"][day]):
        config["description"][day].append("")
    config["description"][day][cl] = description_raw
    with open("config.json", "w") as cf:
        cf.write(json.dumps(config))
    return redirect(url_for("root", day=day, cl=cl))


def getdescription(day, cl):
    if day < len(config["description"]) and cl < len(config["description"][day]):
        return config["description"][day][cl]
    return ""

def getdir(day, cl):
    dirs = ""
    dirs = config["dirs"][day]
    targetdir = ""
    if cl >= 0 and cl < len(dirs):
        targetdir = dirs[cl]
        return targetdir
    return ""

@app.route("/<day>/<cl>/open")
def opendir(day, cl):
    day = int(day)
    cl = int(cl)
    cldir = getdir(day, cl)
    target = os.path.join(rootdir, cldir)
    if cldir and os.path.exists(target):
        try:
            subprocess.Popen(["explorer.exe", target]) #windows
        except:
            try:
                subprocess.Popen(["open", target]) #mac
            except:
                subprocess.Popen(["xdg-open", target]) #linux
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

if __name__=="__main__":
    app.run(port=8000)
