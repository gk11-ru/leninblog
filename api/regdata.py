import rsa, base64, os

def addr_s(addr):
    return ''.join(addr.split())

class udata(object):
    def __init__(self,kvi,redir=''):
        self.redir = redir
        kvitok = kvi.strip().strip(':')
        try:
            data = base64.urlsafe_b64decode(kvitok).splitlines()
            self.uname = data[0]
            self.uaddr = addr_s(data[1])
            self.opts = data[2]
            self.sign = data[3]
            self.kvitok = kvitok
        except:
            self.uname,self.uaddr,self.opts,self.sign,self.kvitok = '','','','',''
    def check(self):
        for ck in os.listdir('keys'):
            pubkey =  rsa.PublicKey.load_pkcs1( open('keys/%s' % ck).read() )
            msg = '%s\n%s\n%s\n' % (self.uname,self.uaddr,self.opts)
            try:
                if rsa.verify(msg,base64.urlsafe_b64decode(self.sign),pubkey):
                    return ck
            except:
                pass
        return ''
