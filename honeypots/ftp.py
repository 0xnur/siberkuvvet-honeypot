'''
https://github.com/alexbredo/honeypot-ftp
'''
import time
import uuid
import json
from twisted.python import filepath
from twisted.protocols.ftp import FTPFactory, FTPRealm, FTP
from twisted.cred.portal import Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.internet import reactor, ssl

class SimpleFtpProtocol(FTP):
    def __init__(self):
        self.session = str(uuid.uuid1())
        self.myownhost = '127.0.0.1'

    def connectionMade(self):
        self.logIt('connected', True)
        ##print('connected', '', True)
        FTP.connectionMade(self)

    def connectionLost(self, reason):
        self.logIt('disconnected', True)
        ##print('disconnected', '', True)
        FTP.connectionLost(self, reason)

    def lineReceived(self, line):
        self.logIt(line, True)
        ##print('command', line, True)
        FTP.lineReceived(self, line)

    # BEGINN HACKS: Do not write anything to disk (Remove Functionality)

    def ftp_STOR(self, path):
        FTP.sendLine(
            self, '125 Data connection already open, starting transfer')
        FTP.sendLine(self, '226 Transfer Complete.')

    def ftp_DELE(self, path):
        FTP.sendLine(self, '250 Requested File Action Completed OK')

    def ftp_RNFR(self, fromName):
        FTP.sendLine(
            self, '350 Requested file action pending further information.')

    def ftp_RNTO(self, toName):
        FTP.sendLine(self, '250 Requested File Action Completed OK')

    def ftp_MKD(self, path):
        FTP.sendLine(self, '257 Folder created')

    def ftp_RMD(self, path):
        FTP.sendLine(self, '250 Requested File Action Completed OK')
    # END HACKS

    def logIt(self, command, successful):
        f = open('/var/log/honeypots/ftp.log', 'a')
        data = {
            'timestamp': int(time.time()),
            'command': command,
            #'session': self.session
        }
        f.write(json.dumps(data)+',\n')
        f.close()


try:
    factory = FTPFactory(
        Portal('./'),
        [FilePasswordDB('./none')]
    )
    factory.protocol = SimpleFtpProtocol
    reactor.listenTCP(21, factory)
    reactor.run()
except Exception as e:
    print(e)
