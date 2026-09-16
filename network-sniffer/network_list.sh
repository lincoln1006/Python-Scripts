#!/bin/bash
test=$(sudo nmap -sn 192.168.0.0/24)
echo $test > output.txt

