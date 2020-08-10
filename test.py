#! /usr/bin/python3
import os
import subprocess
import datetime

os.chdir(os.path.dirname(__file__))

subprocess.call(["git","pull"])

f = open("testText.txt","a+")

f.write("test "+str(datetime.datetime.now())+"\n")

f.close()

subprocess.call(["git","add", "testText.txt"])
subprocess.call(["git", "commit", "-m", "Automation test"])
subprocess.call(["git","push"])
