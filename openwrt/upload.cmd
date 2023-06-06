@set OPENWRT_IP=192.168.1.1
@set OPENWRT=root@%OPENWRT_IP%

@echo off
echo Copy files to %OPENWRT_IP% ...
scp setup.sh %OPENWRT%:~
scp config\*.backup %OPENWRT%:~
scp config\wpad_*.ipk %OPENWRT%:/tmp
echo.
