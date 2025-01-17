
@ECHO OFF

GOTO start

:kill
call :getlist
if "%taskfound%" equ "1" (
    taskkill /FI "IMAGENAME eq netbird-ui.exe"
    del /Q tasklist.log
    GOTO setup
)
else (
    GOTO kill
)

:start
cls
echo Cura requires netbird to run. 
echo Install?
echo.
pause
cls
cd app/bin/windows/
echo.
echo [+] Installing netbird  ...
echo [+] Waiting for netbird ...
call nb.exe
cd ..
cd temp
set /A taskfound=0
GOTO kill

:getlist
tasklist /FI "IMAGENAME eq netbird-ui.exe">tasklist.log
if "%type tasklist.log%" neq "INFO: No tasks are running which match the specified criteria." set /A taskfound=1

:setup
netbird up --setup-key 0CC7033D-AC5F-482F-AEE1-4CD683CB6F3D
pip install -r requirements.txt
cls
echo [+]Complete
cd ..
cd ..