# Enable wireless
uci set wireless.@wifi-device[0].disabled=0
uci commit

# Enable 802.1x authentication
opkg remove wpad-basic-wolfssl
opkg install /tmp/wpad_2022-01-16-cff80b4f-16.2_mipsel_24kc.ipk

# Setup network
cat ~/network.backup > /etc/config/network
cat ~/wireless.backup > /etc/config/wireless
cat ~/dhcp.backup > /etc/config/dhcp
cat ~/firewall.backup > /etc/config/firewall

# Restart DHCP and network manager
service dnsmasq restart
service network restart
