from os import system
import subprocess
import time
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None
proccess = '1'

# tmp = subprocess.Popen(['systemctl', 'status', proccess])
# print(tmp.args)

def start_process() :
    global proccess
    proccess
    tmp = subprocess.Popen(['systemctl', 'status', proccess])
    if proccess is not None and tmp.returncode == 0:
        print("Process already running")
    else :
        print('Proccess not started')
        print('\n',tmp.returncode)
start_process()