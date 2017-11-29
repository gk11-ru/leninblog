import sx

def rf(fn,utf=False):
    ''' read file '''
    try:
        s = open(fn).read()
        if utf:
            return s.decode('utf-8')
        else:
            return s
    except:
        return ''


#def obj_hash(o):
#    ''' make hash for object '''
#    return sx.hsh(bb_transform(o,60))


def obj_to_file(o,sep=1):
    ''' transofm object to ii msg '''
    repto = '/repto/%s' % o.repto if o.repto else ''
    tags = '/tags/%s' % o.tags if o.tags else ''
    header = 'ii/ok%s/topicid/%s%s' % (repto, o.topicid, tags)
    return '%s\n%s\n%s\n%s\n%s\n%s\n%s\n\n%s' % (header, o.ea, int(o.date) // sep, o.who, o.addr, o.to, o.title, o.txt)


def file_to_obj(s):
    ''' transform ii msg to object '''
    pz = s.splitlines()
    o = sx.mydict()
    optz = pz[0].split('/')
    o.update( dict(zip(optz[::2],optz[1::2])) )
    for i,n in enumerate(('ea','date','who','addr','to','title')):
        o[n] = pz[i+1]
    o.txt = '\n'.join(pz[8:])
    o.date = int(o.date) if o.date else sx.gts()
    return o


def wf(fn,s,utf=None):
    if utf:
        s = s.encode('utf-8')
    open(fn,'w').write(s)

def af(fn,s,utf=None):
    if utf:
        s = s.encode('utf-8')
    open(fn,'a').write(s)

def gm(s):
    return rf('data/m/%s' % s)

def lst(ff):
    return rf('data/%s' % ff).splitlines()
