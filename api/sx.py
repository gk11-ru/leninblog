# -*- coding: utf-8 -*-

import time, bottle, base64, hashlib, re
from splitparser import sp

class mydict(dict):
    def __getattr__(self, key):
        return self.get(key,'')
    def __setattr__(self, key, value):
        self[key] = value
    def __add__(self, data):
        return mydict(self.items() + data.items())
    def __sub__(self, key):
        return mydict((k,v) for (k,v) in self.items() if k != key)

def hsh(s):
    #return base64.urlsafe_b64encode( hashlib.sha256(s).digest() ).replace('-','A').replace('_','z')[:20]
    return base64.b32encode(hashlib.sha256(s).digest())[:20]

def datef(d,f):
    return time.strftime(f, time.localtime(int(d)))

def dateg(d,f='%d.%m.%y %H:%M'):
    return time.strftime(f, time.gmtime(int(d)))

def tri_fmt(tx,tri=[u'комментарий',u'комментария',u'комментариев']):
    if tx % 100 in range(10,21): return unicode(tx) + u' ' + tri[2]
    return unicode(tx) + u' ' + tri[{2:1,3:1,4:1,1:0}.get(tx % 10,2)]

def gts():
    return int(time.time())

def rend(txt,image=False):
    out = bottle.html_escape(txt)
    out = sp(out,image)
    return out.replace('\n', '<br />')

def b64c(s):
    return base64.b64encode(s)

def b64u(s):
    return base64.urlsafe_b64encode(s)

def b64d(s):
    return base64.b64decode( s.replace('-','+').replace('_','/') )

def b32c(s):
    return base64.b32encode(s)

def b32d(s):
    return base64.b32decode(s)

def echo_flt(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{3,120}$')
    if rr.match(ea) and '.' in ea: return True

def msg_flt(msgid):
    rr = re.compile(r'^[a-z0-9A-Z]{20}$')
    if rr.match(msgid): return True
