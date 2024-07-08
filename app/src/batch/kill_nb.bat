@ECHO OFF


GOTO kill


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

:getlist
tasklist /FI "IMAGENAME eq netbird-ui.exe">tasklist.log
if "%type tasklist.log%" neq "INFO: No tasks are running which match the specified criteria." set /A taskfound=1

:setup
netbird up --setup-key 0CC7033D-AC5F-482F-AEE1-4CD683CB6F3D
cls