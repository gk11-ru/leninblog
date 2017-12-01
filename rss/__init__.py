import api, api.sx as sx, datetime
import conf

def gen_topic(topicid,num=30):
    comms = api.lst('topic/%s' % topicid)
    ea = comms[2]
    tdesc = comms[1]
    comms = comms[6:]
    msgs = [api.get_msg(n) for n in reversed(comms[-num:])]
    items = [PyRSS2Gen.RSSItem(
        title=n.title,description=sx.rend(n.txt.decode('utf-8')),
        link='%s/msg/%s#go_%s' % (conf.URL,topicid,n.msgid),
        guid='%s/msg/%s#go_%s' % (conf.URL,topicid,n.msgid),
        author=n.who,
        pubDate=datetime.datetime.fromtimestamp(n.date)
    ) for n in msgs ]
    rssout = PyRSS2Gen.RSS2(title=ea,link='%s/msg/%s' % (conf.URL,topicid),description=tdesc,
    lastBuildDate=datetime.datetime.now(),items=items)
    return rssout.to_xml('utf-8')

def gen_blog(ea,num=30):
    comms = api.get_ea(ea)
    msgs = [api.get_msg(n) for n in reversed(comms[-num:])]
    items = [PyRSS2Gen.RSSItem(
        title=n.title,description=sx.rend(n.txt.decode('utf-8')),
        link='%s/msg/%s' % (conf.URL,n.msgid),
        guid='%s/msg/%s' % (conf.URL,n.msgid),
        author=n.who,
        pubDate=datetime.datetime.fromtimestamp(n.date)
    ) for n in msgs ]
    rssout = PyRSS2Gen.RSS2(title=ea,link='%s/blog/%s' % (conf.URL,ea),description='%s: %s' % (ea,api.echo_desc(ea)),
    lastBuildDate=datetime.datetime.now(),items=items)
    return rssout.to_xml('utf-8')

def gen_all(ea,num=30):
    comms = api.get_ea(ea)
    msgs = [api.get_msg(n) for n in reversed(comms[-num:])]
    items = [PyRSS2Gen.RSSItem(
        title=n.title,description=sx.rend(n.txt.decode('utf-8')),
        link='%s/msg/%s#go_%s' % (conf.URL,n.topicid,n.msgid),
        guid='%s/msg/%s#go_%s' % (conf.URL,n.topicid,n.msgid),
        author=n.who,
        pubDate=datetime.datetime.fromtimestamp(n.date)
    ) for n in msgs ]
    rssout = PyRSS2Gen.RSS2(title=ea,link='%s/blog/%s' % (conf.URL,ea),description='%s: %s' % (ea,api.echo_desc(ea)),
    lastBuildDate=datetime.datetime.now(),items=items)
    return rssout.to_xml('utf-8')

def lastcomm(ea,num,userdir=''):
    if ea:
        dl = api.lst('e/%s' % ea)
    else:
        dl = [n.split()[0] for n in api.lst('m.accepted')]
    if userdir:
        dl = [n for n in api.lst('carbon/%s' % userdir) if n in dl]
    cntr = 0
    msgs = []
    for n in reversed(dl):
        tmp = api.get_msg(n)
        if tmp.repto:
            msgs.append(tmp)
            cntr += 1
        if cntr >= num:
            break
    return msgs
