import platform
import subprocess
import shlex


print("This program relies on external libraries to work!")
process=None

#install netbird and configure

if platform.system() == 'Linux':
    command_str = 'curl -fsSL https://pkgs.netbird.io/install.sh | sh'
    command = shlex.split(command_str)
    process = subprocess.Popen(command , shell=True , stdout=subprocess.PIPE , stderr=subprocess.PIPE)
elif platform.system() == 'windows':
    process=subprocess.Popen(['/bin/windows/nb.exe'] ,shell=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE)

process.wait()
output = process.stdout.read().decode()
err = process.stderr.read().decode()

if err=="":
    print('Netbird installed successfully')
else:
    raise Exception(err)

#Kill netbird gui
