
import subprocess


print("This program relies on netbird")
process=None

#install netbird and configure
process = subprocess.Popen(['app/bin/windows/nb.exe'] ,shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE)
process.wait()
process = subprocess.Popen('app/src/batch/kill_nb.bat')
process.wait()