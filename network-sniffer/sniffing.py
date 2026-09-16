import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
starttime = time.time()
numPackets = 0
with open("packetlog.txt", "w") as f:
	while True:
		f.write(f"{s.recvfrom(65565)}\n")
		curtime = time.time()
		if round(curtime - starttime, 1) > 10:
			exit()
