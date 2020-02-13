#!/bin/bash
set -e
echo "
This project has been developed for experimental purposes. It will perform the following operations on your system:
- Adding and running the Siberkuvvet honeypot as a service
- Adding and running FTP, SSH, Telnet honeypots as a service
- Clear all firewall rules
- Direct all requests (including port 22,80 except port 1) to the honeypot service (local 4141).
- Be sure you install dependencies for all python files.
- It can cause some network access lose.

******  DO NOT USE ON PRODUCTION SYSTEMS ***********
"
read -p "Are you sure you wish to continue? - yes / no"
if [ "$REPLY" != "yes" ]; then
   exit
fi
dir=`pwd`
siberkuvvet_honeypot="
[Unit]
Description=Siberkuvvet Honeypot
[Service]
Type=simple
ExecStart=/usr/bin/python3 $dir/main.py > /dev/null 2>/dev/null
Restart=always
RestartSec=2

[Install]
WantedBy=sysinit.target
"
ftp_honeypot="
[Unit]
Description=FTP Honeypot
[Service]
Type=simple
ExecStart=/usr/bin/python $dir/honeypots/ftp.py > /dev/null 2>/dev/null
Restart=always
RestartSec=2

[Install]
WantedBy=sysinit.target
"

telnet_honeypot="
[Unit]
Description=Telnet Honeypot
[Service]
Type=simple
ExecStart=/usr/bin/python $dir/honeypots/telnet.py > /dev/null 2>/dev/null
Restart=always
RestartSec=2

[Install]
WantedBy=sysinit.target
"

ssh_honeypot="
[Unit]
Description=SSH Honeypot
[Service]
Type=simple
ExecStart=/usr/bin/python $dir/honeypots/ssh.py > /dev/null 2>/dev/null
Restart=always
RestartSec=2

[Install]
WantedBy=sysinit.target
"
echo "\n\n\n"
echo "creating services...";
echo "$siberkuvvet_honeypot" > /etc/systemd/system/siberkuvvet_honeypot.service
echo "$ftp_honeypot" > /etc/systemd/system/ftp_honeypot.service
echo "$telnet_honeypot" > /etc/systemd/system/telnet_honeypot.service
echo "$ssh_honeypot" > /etc/systemd/system/ssh_honeypot.service
systemctl daemon-reload
systemctl enable siberkuvvet_honeypot && systemctl start siberkuvvet_honeypot --no-block
systemctl enable ftp_honeypot && systemctl start ftp_honeypot --no-block
systemctl enable telnet_honeypot && systemctl start telnet_honeypot --no-block
systemctl enable ssh_honeypot && systemctl start ssh_honeypot --no-block

iptables -F -t nat
sysctl -w net.ipv4.conf.eth0.route_localnet=1
iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 2:65530 -j DNAT --to-destination 127.0.0.1:4141

mkdir -p /var/log/honeypots/
touch /var/log/honeypots/ftp.log
touch /var/log/honeypots/telnet.log
touch /var/log/honeypots/ssh.log


# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' ERR
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' ERR
