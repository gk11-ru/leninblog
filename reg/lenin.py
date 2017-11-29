# -*- coding: utf-8 -*-

import api, os

def pdir(s):
    try:
        os.mkdir(s)
    except:
        pass

def touch(s,z=False):
    open(s,'w' if z else 'a').write()

def unlist(fn,itm):
    out = api.lst(fn)
    if itm in out:
        out.remove(itm)
    if out:
        open(fn,'w').write('\n'.join(out) + '\n')
    else:
        os.remove(fn)
        return True

def unm(itm):
    out = api.lst('data/m.accepted')
    for n in out:
        mid,ts = n.split()
        if mid == itm:
            out.remove(n)
            if out:
                open('data/m.accepted','w').write('\n'.join(out) + '\n')
            else:
                open('data/m.accepted','w').write('')
            return True

def del_msg(itm):
    if not unm(itm):
        return
    o = api.get_msg(itm)
    unlist('carbon/%s' % api.hsh(o.to.encode('utf-8')), itm)
    unlist('carbon/_%s' % api.hsh(o.who.encode('utf-8')), itm)
    unlist('e/%s' % o.ea, itm)
    unlist('et/%s' % o.ea, itm)
    #need remove from tags!
    print o.tags
    os.remove('m/%s' % itm)

def create_account():
    pdir('data')
    for n in ('m', 'e', 'et', 'topic', 'carbon', 'tags', 'ntag', 'nuser'):
        pdir ('data/%s' % n)
    touch('data/blacklist.txt')
    touch('data/m.accepted')


def check_adm(s_):
    s = s_.encode('utf-8')
    if s and s == api.rf('data/admikey.txt'):
        return s

