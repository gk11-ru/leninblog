import api, api.sx as sx, datetime
from api.bottle import template
import conf

def msglst(l,num):
    out = []
    for x in reversed(l[-num:]):
        n = api.get_msg(x)
        n.update({'url': '%s/msg/%s#go_%s' % (conf.URL,n.topicid,n.msgid),'pubDate': datetime.datetime.fromtimestamp(n.date)})
        out.append(n)
    return out


def gen_topic(topicid,num=30):
    comms = api.lst('topic/%s' % topicid)
    ea, desc = comms[2], comms[1]
    return template('rss/rss.tpl',msgs=msglst(comms[6:],num),title=ea,link='%s/msg/%s' % (conf.URL,topicid),desc=desc)


def gen_blog(ea,num=30):
    topics = set(api.lst('topic.list'))
    comms = [x for x in api.get_ea(ea) if x in topics]
    return template('rss/rss.tpl',msgs=msglst(comms,num),title=ea,link='%s/blog/%s' % (conf.URL,ea),desc='%s: %s' % (ea,api.echo_desc(ea)))


def gen_all(ea,num=30):
    comms = api.get_ea(ea)
    return template('rss/rss.tpl',msgs=msglst(comms,num),title=ea,link='%s/blog/%s' % (conf.URL,ea),desc='%s: %s' % (ea,api.echo_desc(ea)))


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
