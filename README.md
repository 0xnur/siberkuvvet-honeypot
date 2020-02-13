Türkçe açıklama için https://siberkuvvet.com/p/siberkuvvet-balkupu

# siberkuvvet honeypot with protocol detection
This repo contains experimental codes for siberkuvvet honeypots. 

It run as a services. Get all request from all ports with iptables rules. 
Create a services for each requests. 
Do protocol detection from first request bytes. 
Redirect traffic to running honeypots.

For production with high load some other services must be implemented such as haproxy, kubernates, dockers, librenms, kibana, elasticsearch, etc.

Default honeypots:
**FTP honeypot :** https://github.com/alexbredo/honeypot-ftp
**SSH honeypot :** https://github.com/idleninja/ssh_honeypot-ish/blob/master/simplesshserver_creds.py
**Telnet honeypot :** https://github.com/mbologna/telnetd_honeypot/blob/master/telnetd.py
**HTTP honeypot :** Apache2 with modsecurity

#Install
**Do not install this repo on production systems.**

bash install.sh

## Useful Commands
## iptables and network commands
clear all nat rules and redirect all port to local 4141 ports (interface name can be different)



    iptables -F -t nat
    net.ipv4.ip_forward = 1 
    sysctl -w net.ipv4.conf.eth0.route_localnet=1
    iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 1:65530 -j DNAT --to-destination 127.0.0.1:4141

## apache2 HTTP honeypot

    apt-get install apache2
    apt-get install libapache2-mod-security2 
    echo "" > /var/www/html/index.html 

add this to /etc/apache2/sites-enabled/000-default.conf <br>
> <Directory /var/www/html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
</Directory>



add this to  /etc/apache2/apache2.conf to log post method details: <br>
> RewriteEngine on 
RewriteRule ^(.*)$ index.html [QSA,L] 
SecRuleEngine On 
SecAuditEngine on 

> \#Setup logging in a dedicated file. 
SecAuditLog /var/log/apache2/honeypot.log 
\#Allow it to access requests body. 
SecRequestBodyAccess on 
SecAuditLogParts ABCZ
\#Setup default action. 
SecDefaultAction "nolog,noauditlog,allow,phase:2"
\#Define the rule that will log the content of POST requests.
SecRule REQUEST_METHOD "^POST$" "chain,allow,phase:2,id:123"
SecRule REQUEST_URI ".*" "auditlog




#### DEBUG
show network

    watch -n 1 "netstat -antp | grep -v tcp6 | egrep ':4141|0.0.0.0:2222|0.0.0.0:80|0.0.0.0:21|0.0.0.0:23'"
