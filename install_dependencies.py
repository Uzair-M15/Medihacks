
import subprocess


print("This program relies on netbird")
process=None

#install netbird and configure
process = subprocess.Popen(['/bin/windows/nb.exe'] ,shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE)
process.wait()
process = subprocess.Popen('/src/batch/kill_nb.bat')
process.wait()