@echo off
cls

python %~dp0nbz_interface.py -s %1

del %~dp0server.log
del %~dp0bmp.log
del %~dp0geckodriver.log

python %~dp0close_all.py