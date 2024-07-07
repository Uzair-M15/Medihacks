@ECHO OFF

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
