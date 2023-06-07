# 2023 CNL Final Project

## Web Server

- Install MySQL server
- Clone this repo
- Install Python packages
- `cd 2023cnl_final_project/web_server` and run `python3 web_server.py`
- Open browser and type `192.168.1.2:17171`

## VLAN Setup

### RADIUS Server

#### Environment

- Set `bridge adapter` connect to router
- Set static IP address `192.168.1.3`

#### EAP

- Enable PEAP authentication
- Edit `/etc/freeradius/3.0/mods-available/eap`
    ```bash
    peap {
    	...
    	use_tunneled_reply = yes
    	...
    }
    ```

> Or you can just copy the `freeradius-config` directory to your RADIUS server

#### VLAN Setting

- Teacher VLAN number: `1`
- Student VLAN number: `3`

### OpenWrt

Ensure that the router is already connected to your host.

#### On Host

- Copy required files onto router
    ```bash
    # On WINDOWS device
    cd openwrt
    .\upload.cmd
    ```

#### On Router

- `ssh` into router
    ```bash
    ssh root@192.168.1.1
    ```
- Setup
    ```bash
    bash setup.sh
    ```
- Open `192.168.1.1` through browser to check that the setting is correct
    - Or `ssh` again and check by
        ```bash
        brctl show
        ```
