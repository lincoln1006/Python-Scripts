import subprocess
import time

class Device:
    def __init__(self, name, mac, ip):
        self.name = name
        self.mac = mac
        self.ip = ip

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
textSplit = text.split(" ")
f.close()
i = 10
newDevice = False
devices = []
while i < len(textSplit) - 1:
    try:
        if textSplit[i] == "Nmap" and textSplit[i+1] == "scan":
            newDevice = True
            ip = textSplit[i+4]
            mac = textSplit[i+12]
            i += 12
            nameDone = False
            name = ""
            while nameDone == False:
                if textSplit[i][-1] == ")":
                    name += textSplit[i]
                    nameDone = True
                else:
                    name += f"{textSplit[i]} "
                    i+=1
            devices.append(Device(name, mac, ip))
        i+=1
    except:
        break
with open("output.txt", "w") as f:
    for val in devices:
        f.write(f"Device: {val.name}\nMac Address: {val.mac}\n IP Address: {val.ip}\n")


