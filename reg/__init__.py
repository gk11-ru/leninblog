# -*- coding: utf-8 -*-

import rsa, base64, time, hashlib
privkey =  rsa.PrivateKey.load_pkcs1( open('data/priv.key').read() )

ADDR='lenina'

def _uflt(u):
    return ' '.join(u.split())

def kvi_sign(user,addr,uid,ts):
    k = '%s\n%s,%s\nts/%s\n' % (user,addr,uid,ts)
    signature = rsa.sign(k, privkey, 'SHA-1')
    s = k + base64.urlsafe_b64encode(signature)
    return base64.urlsafe_b64encode(s)

def mk_reg(rq):
    user = _uflt(rq.uname.encode('utf-8'))
    if not user:
        return u'имя не задано'
    if rq.upass2 and rq.ucheck != '51':
        return u'это не пятьдесят один'
    pass1 = rq.upass1.encode('utf-8')
    if not pass1:
        return u'нет пароля'
    pass1 = hashlib.sha1(pass1).hexdigest()
    udb =  open('data/points.txt').read().splitlines()
    uid = None
    for i,n in enumerate(udb):
        uif = n.split(':',3)
        if uif[1] == pass1 and uif[2] == user:
            uid = i+1
            ts = uif[0]
            break
        elif uif[2] == user and uif[1] != pass1:
            return u'Пользователь уже существует. А его пароль - нет'
    if uid is None:
        if rq.upass1 != rq.upass2:
            return u'два разных пароля, вы уж определитесь',
        ts = int(time.time())
        open('data/points.txt', 'a').write('%s:%s:%s\n' % (ts,pass1,user))
        uid = open('data/points.txt').read().splitlines().index('%s:%s:%s' % (ts,pass1,user)) + 1
    kvitok = kvi_sign(user,ADDR,uid,ts)
    return ':' + kvitok + ':'
