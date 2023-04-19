from os import system
import subprocess
import time
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None

tmp = subprocess.Popen(['systemctl', 'status', '158534'])
print(tmp.args)

# def start_process() :
#     global proccess
#     if proccess is not None and proccess.poll() is None:
#         print("Process already running")
#     else :
#         print('Proccess not started')
# start_process()