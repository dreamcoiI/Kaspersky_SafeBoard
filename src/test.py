from os import system
import subprocess
import time
import psutil
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None
proccess = '1'

# tmp = subprocess.Popen(['systemctl', 'status', proccess])
# print(tmp.args)

def start_process() :
    global proccess
    proccess
    pid = int(proccess)
    tmp = subprocess.Popen(['systemctl', 'status', proccess])
    if tmp.returncode is None and psutil.pid_exists(pid):
        print("Process already running")
    else :
        print('Proccess not started')
start_process()