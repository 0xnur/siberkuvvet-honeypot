'''
https://github.com/mbologna/telnetd_honeypot/blob/master/telnetd.py
'''
from twisted.internet import protocol, reactor, endpoints
import logging
import random
import time
import json
import string

class Telnetd(protocol.Protocol):
    PROMPT = "switch for eks private_network# "
    def dataReceived(self, data):
        data = data.strip()
        if data == "id":
            self.transport.write("uid=0(root) gid=0(root) groups=0(root)\n")
        elif data.split(" ")[0] == "uname":
            self.transport.write("Linux f001 3.13.3-7 #3000-EKS SMPx4 Jun 31 25:24:23 UTC 2200 x86_64 x64_86 x13_37 GNU/Linux\n")
        else:
            if random.randrange(0, 2) == 0 and data != "":
                self.transport.write("bash: " +  data.split(" ")[0] + ": command not found\n")
        time.sleep(1)
        self.transport.write(Telnetd.PROMPT)

        if data != "":
            if all(c in string.printable for c in data):
                self.logIt(data)
            #self.logIt(data)

    def connectionMade(self):
        self.transport.write(Telnetd.PROMPT)

    def logIt(self, command):
        f = open('/var/log/honeypots/telnet.log', 'a')
        data = {
            'timestamp': int(time.time()),
            'command': str(command).decode('utf-8'),
            #'session': self.session
        }
        f.write(json.dumps(data, encoding='utf-8')+',\n')
        f.close()


class TelnetdFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Telnetd()

endpoints.serverFromString(reactor, "tcp:23").listen(TelnetdFactory())
reactor.run()
