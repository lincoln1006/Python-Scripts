import subprocess
import time
subprocess.run(["./network_list.sh"])
outputRead = False
attempts = 0
while outputRead == False:
    try:
        attempts += 1
        f = open("output.txt", "r")
        outputRead = True
    except:
        print("output.txt not found")
        time.sleep(1)
    if attempts > 15:
        print("script failed, exiting now")
        exit()
text = f.readlines()
f.close()
