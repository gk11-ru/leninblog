# -*- coding: utf-8 -*-

import api, os, rsa

def pdir(s):
    try:
        os.mkdir(s)
    except:
        pass

def touch(s,z=False):
    open(s,'w' if z else 'a').write('')

def unlist(fn,itm):
    print fn, itm
    out = api.lst(fn)
    print out
    if itm in out:
        out.remove(itm)
        print out
        if out:
            open('data/' + fn,'w').write('\n'.join(out) + '\n')
        else:
            os.remove('data/' + fn)
            return True

def unm(itm):
    out = api.lst('m.accepted')
    for n in out:
        mid,ts = n.split()
        if mid == itm:
            out.remove(n)
            if out:
                open('data/m.accepted','w').write('\n'.join(out) + '\n')
            else:
                open('data/m.accepted','w').write('')
            return True

def del_from_tags(itm):
    for n in os.listdir('data/tags'):
        unlist('tags/' + n, itm)

def del_msg(itm):
    if not unm(itm):
        return
    o = api.get_msg(itm)
    unlist('carbon/%s' % api.hsh(o.to.encode('utf-8')), itm)
    unlist('carbon/_%s' % api.hsh(o.who.encode('utf-8')), itm)
    unlist('e/%s' % o.ea, itm)
    unlist('et/%s' % o.ea, itm)
    unlist('topic/%s' % o.topicid, itm)
    os.remove('data/m/%s' % itm)

def del_all(itm):
    if api.lst('topic/%s' % itm):
        del_from_tags(itm)
        for n in api.lst('topic/%s' % itm)[5:]:
            del_msg(n)
        unlist('topic.list',itm)
        touch('data/topic.list')
        os.remove('data/topic/%s' % itm)
    else:
        del_msg(itm)

def create_account(rq):
    addr = ''.join(rq.addr.split())
    ea = ''.join(rq.ea.split())
    if not '.' in rq.ea:
        return u'не хватает точки в имени эхи'
    pdir('data')
    (pubkey, privkey) = rsa.newkeys(368)
    open('data/priv.key','w').write( privkey.save_pkcs1() )
    pdir('keys')
    open('keys/pub.key','w').write( pubkey.save_pkcs1() )

    for n in ('m', 'e', 'et', 'topic', 'carbon', 'tags', 'ntag', 'nuser'):
        pdir ('data/%s' % n)
    bufu = u'%s\n%s\n%s\n%s\n%s\n%s\n' % (rq.brand, rq.tagline, rq.ea, rq.addr, rq.url, rq.desc)
    open('data/config','w').write(bufu.encode('utf-8'))
    open('data/e.list','w').write('%s\n' % rq.ea.encode('utf-8'))
    open('data/e.desc','w').write('%s %s\n' % (rq.ea.encode('utf-8'), rq.eadesc.encode('utf-8')))
    open('data/admikey.txt','w').write(rq.akey.encode('utf-8'))


def check_adm(s_):
    s = s_.encode('utf-8')
    if s and s == api.rf('data/admikey.txt'):
        return s

