
import subprocess


print("This program requires netbird and python")
process=None

#install netbird and configure
print("[-]Installing Netbird")
process = subprocess.Popen(['app/bin/windows/nb.exe'] ,shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE)
process.wait()
no_error = process.stderr.read().decode() == ''
print(process.stdout.read().decode())
print("[-]Killing netbird-gui\n")
process = subprocess.Popen('cd app && cd src && cd batch && kill_nb.bat' , shell=True , stdout=subprocess.PIPE , stderr = subprocess.PIPE)
process.wait()
no_error = (process.stderr.read().decode()== '') and (no_error)
print(process.stdout.read().decode())
if no_error:
    print("[+]Installed successfully")
else:
    print("[!]An error occured. The installation could be broken")