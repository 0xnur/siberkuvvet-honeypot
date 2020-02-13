class TCP_Protocol_Detection:
        def __init__(self,first_bytes):
            """Take first bytes of request. This is after handshake"""
            self.first_bytes = first_bytes

        def honeypot_port(self):
            """ Return protocol number defined top of main.py"""
            return self.is_HTTP() or \
                    self.is_SSH() or \
                    self.is_FTP() or \
                    self.is_SMTP() or \
                    23

        def is_HTTP(self):
            """ check if first bytes are HTTP Request"""
            if self.first_bytes.startswith((b'GET', b'POST', b'OPTIONS', b'HEAD', b'PUT', b'TRACE')):
                return 80
            return False

        def is_SSH(self):
            """ check if first bytes are SSH Request"""
            if self.first_bytes.startswith(b'SSH'):
                return 2222
            return False

        def is_SMTP(self):
            """ check if first bytes are SMTP Request"""
            if self.first_bytes.startswith(b'EHLO'):
                return 25
            return False

        def is_FTP(self):
            """ check if first bytes are FTP Request"""
            if self.first_bytes.upper().startswith((b'BOR',b'ACCT',b'ADAT',b'ALLO',b'APPE',b'AUTH', \
                b'AVBL',b'CCC',b'CDUP',b'CONF',b'CSID',b'CWD',b'DELE',b'DSIZ',b'ENC',b'EPRT',b'EPSV',b'FEAT',b'HELP',b'HOST',\
                b'LANG',b'LIST',b'LPRT',b'LPSV',b'MDTM',b'MFCT',b'MFF',b'MFMT',b'MIC',b'MKD',b'MLSD',b'MLST',b'MODE',b'NLST',b'NOOP',\
                b'OPTS',b'PASS',b'PASV',b'PBSZ',b'PORT',b'PROT',b'PWD',b'QUIT',b'REIN',b'REST',b'RETR',b'RMD',b'RMDA',b'RNFR',b'RNTO',\
                b'SITE',b'SIZE',b'SMNT',b'SPSV',b'STAT',b'STOR',b'STOU',b'STRU',b'SYST',b'THMB',b'TYPE',b'USER',b'XCUP',b'XMKD',b'XPWD',\
                b'XRCP',b'XRMD',b'XRSQ',b'XSEM',b'XSEN')):
                return 21
            return False
