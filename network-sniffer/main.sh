echo "running linux_bash.py"
sudo python linux_bash.py
echo "running sniff_test.py"
sudo python sniff_test.py
echo "pushing log files"
git add .
git commit -m "test auto commit with .sh file, pushing output from multiple scripts"
git push
git pull
