# -*- coding: utf-8 -*-

from sx import mydict, gts, hsh, b64u, msg_flt, echo_flt, b64d
import fo, msghook
from fo import gm, lst, rf, wf, af

def check_check(rq):
    if not all([rq.txt,rq.title,rq.ea,rq.to]):
        print dict(rq)
        return
    rq.tags = rq.tags.strip()
    rq.title = rq.title.strip()
    rq.txt = rq.txt.strip()
    if rq.ea not in lst('e.list'):
        print 'elist'
        print rq.ea
        return
    if rq.msgid != rq.topicid:
        if rq.topicid and not rq.topicid in lst('topic.list'):
            print 'topiclist'
            print rq.topicid
            return
    return rq


def mk_tags(s):
    tags = [x.strip().lower().encode('utf-8') for x in s.split(',')]
    return ','.join([b64u(x) for x in tags])


def write_msg(o,msgid,blob,date,newflag):
    wf('data/m/%s' % msgid , blob)
    af('data/e/%s' % o.ea, '%s\n' % msgid)
    af('data/m.accepted', '%s %s\n' % (msgid,date))
    wf('data/nuser/%s' % hsh(o.who.encode('utf-8')), o.who.encode('utf-8'))
    wf('data/nuser/%s' % hsh(o.to.encode('utf-8')), o.to.encode('utf-8'))
    af('data/carbon/_%s' % hsh(o.who.encode('utf-8')), '%s\n' % msgid)
    af('data/carbon/%s' % hsh(o.to.encode('utf-8')), '%s\n' % msgid)
    if msgid != o.topicid:
        af('data/topic/%s' % o.topicid, '%s\n' % msgid)
    else:
        af('data/topic.list','%s\n' % msgid)
        af('data/et/%s' % o.ea, '%s\n' % msgid)
        wf('data/topic/%s' % msgid, u'%s\n%s\n%s\n%s\n%s\n%s\n' % (o.date,o.title,o.ea,o.who,o.addr,msgid),True)
        if o.tags:
            for n in o.tags.split(','):
                wf('data/ntag/%s' % hsh(n), b64d(n))
                af('data/tags/%s' % hsh(n), '%s\n' % msgid)


def create_msg(rq_raw,u):
    ''' create msg from user form '''
    rq = check_check(rq_raw)
    date = str(gts())
    txt=rq.txt
    if rq.pic:
        for n in rq.pic.split():
            txt += '\n\n@image: %s' % n
    o = mydict(txt=txt,title=rq.title,date=date,ea=rq.ea,who=u.uname,addr=u.uaddr,to=rq.to)
    if rq.repto:
        o.repto=rq.repto
    if rq.tags and not rq.topicid:
        o.tags = mk_tags(rq.tags)
    blob = fo.obj_to_file(o,60).encode('utf-8')
    msgid = hsh(blob)
    o.topicid = rq.topicid or msgid
    o = msghook.hook(o,True)
    blob = fo.obj_to_file(o).encode('utf-8')
    write_msg(o,msgid,blob,date,True)
    return msgid


def accept_msg(rq_raw):
    ''' accept msg from fetcher '''
    rq = check_check(rq_raw)
    if rq:
        date = str(gts())
        msgid = rq.msgid
        if not msg_flt(msgid):
            return
        o = rq
        blob = fo.obj_to_file(o).encode('utf-8')
        write_msg(o,msgid,blob,date,True)
        return msgid


def echolist():
    return lst('e.list')

def echo_desc(e):
    return mydict([x.split(' ',1) for x in lst('e.desc')]).get(e, 'no desc')


def forum_list(e):
    out = []
    for n in lst('et/%s' % e):
        fi = mydict(topic=lst('topic/%s' % n))
        o = get_msg(fi.topic[-1])
        fi.lastdate, fi.lastuser = o.date, o.who
        out.append(fi)
    out.sort(key=lambda a: int(a.lastdate))
    return out

def forums_list():
    return [(n,forum_list(n)) for n in echolist()]

def get_msg(mid):
    return fo.file_to_obj(gm(mid)) + {'msgid': mid}

def get_ea(ea):
    return lst('e/%s' % ea)
