# -*- coding: utf-8 -*-

import api
from api.sx import mydict, gts, hsh, b64c, b64d
from api.bottle import route, run, request, response, template, static_file, post, redirect, HTTPError
from api.regdata import udata
import conf, reg, rss
from reg import lenin

def u():
    return udata(request.cookies.kvitok.encode('utf-8'))

def ak():
    return lenin.check_adm(request.cookies.admikey)

@route('/',method=['GET', 'POST'])
def default_blog():
    print conf.f
    if conf.f:
        redirect ('/blog/%s' % conf.EA)
    else:
        if request.method=='POST':
            out = lenin.create_account(request.forms)
            if out:
                return out
            else:
                conf.reload_cfg()
                return u'<a href="/">блог создан</a>'
        else:
            return template('reg/wizard.tpl',conf=conf)


@route('/start')
def start_page():
    mo = [x.split()[0] for x in reversed(api.lst('m.accepted'))]
    return template('start.html',out=api.forums_list(),mo=mo,u=u())

@route('/favicon.ico')
def no_favicon():
    raise HTTPError(404)

@route('/<raw:re:e|m>/<oid>')
def raw_file(raw,oid):
    response.content_type = 'text/plain; charset=utf-8'
    return api.rf('data/%s/%s' % (raw,oid))

@route('/u/e/<f:path>')
def echo_bundle(f):
    response.content_type = 'text/plain; charset=utf-8'
    out = []
    for n in [x for x in f.split('/') if '.' in x]:
        out.append(n)
        out += [x for x in api.get_ea(n)]
    return '\n'.join(out)

@route('/u/all')
def all_bundle():
    response.content_type = 'text/plain; charset=utf-8'
    out = ''
    el, fl = {}, api.lst('e.list')
    for ea in fl:
        el[ea] = api.get_ea(ea)
    for n in [x.split()[0] for x in api.lst('m.accepted')]:
        for ea in fl:
            if n in el[ea]:
                out += '%s:%s\n' % (n,ea)
                break
    return out

@route('/u/m/<f:path>')
def msg_bundle(f):
    response.content_type = 'text/plain; charset=utf-8'
    return '\n'.join(['%s:%s' % (n, b64c(api.gm(n))) for n in f.split('/')]) + '\n'

@route('/list.txt')
def list_txt():
    out = ''
    response.content_type = 'text/plain; charset=utf-8'
    for n in api.echolist():
        out += '%s:%s:%s\n' % (n, len(api.get_ea(n)), api.echo_desc(n) or 'no desc')
    return out

@route('/select-blog')
def blog_select():
    return template ('select-blog.html',u=u(),ea='',out = [(n, len(api.lst('e/%s' % n)), api.echo_desc(n) or 'no desc') for n in api.echolist()])

@route('/blog/<ea>')
def blog_list(ea):
    blogs = api.lst('et/%s' % ea)
    comms = mydict({n:len(api.lst('topic/%s' % n))-6 for n in blogs})
    pge = request.query.page or '1'
    return template ('blog-list.html',u=u(),ea=ea,blogs=blogs,comms=comms,pge=int(pge)-1)

@route('/msg/<topicid>')
def blog_topic(topicid):
    topic = api.lst('topic/%s' % topicid)
    mo = [api.get_msg(n) for n in topic[5:]]
    return template ('blog-topic.html',mo=mo,u=u(),admikey=ak())

@route('/print/<topicid>')
def print_topic(topicid):
    topic = api.lst('topic/%s' % topicid)
    return template ('print.html',jd=api.get_msg(topic[5]),u=u())

@route('/tag/<tag>')
def blog_tag(tag):
    blogs = api.lst('tags/%s' % hsh(tag))
    comms = mydict({n:len(api.lst('topic/%s' % n))-6 for n in blogs})
    msgs = mydict({n:api.get_msg(n) for n in blogs})
    return template ('blog-list.html',blogs=blogs,msgs=msgs,comms=comms,tag=tag,ea='',pge=-1,u=u())

@route(['/lastcomm/','/lastcomm/<ea>'])
def last_comm(ea=''):
    return template('lcomm.html',ea=ea,comms=rss.lastcomm(ea,30),u=u(),admikey=ak())

@route('/carbon/<di:re:from|to|news>/<ea>/<un:path>')
@route('/carbon/<di:re:from|to|news>//<un:path>')
def carbon_area(di,un,ea=''):
    if di in ('from', 'to'):
        uh = hsh(un) if di == 'to' else '_' + hsh(un)
        comm = rss.lastcomm(ea,20,uh)
        return template('reg/lastcomm.html',uname=un,comms=comm,u=u(),admikey=ak(),ea=ea)
    elif di == 'news':
        topic = api.lst('et/%s' % ea) if ea else api.lst('topic.list')
        um = set(api.lst('carbon/_' + hsh(un)))
        return template('reg/lastnews.html',uname=un,news=[x for x in topic if x in um][-15:],u=u(),ea=ea)

@route('/new/blog/<ea>/<topicid>/<repto>')
def reply_form(ea,topicid,repto):
    if repto and repto != '-':
        prev = api.get_msg(repto)
    else:
        prev = mydict()
    return template('frmnews.html',u=u(),prev=prev,typ='blog',ea=ea,topicid=topicid,repto=repto)

@post('/new')
def create_message():
    ud = udata(request.forms.kvitok.encode('utf-8'))
    if not ud.check() or not ud.uname:
        return u'доступ не подтверждён, сочувствуем'
    nmsg = api.create_msg(request.forms,ud)
    if request.forms.typ == 'echo':
        redirect ('/echo/%s#go_%s' % (request.forms.ea, nmsg))
    else:
        redirect ('/%s/%s#go_%s' % (dict(forum='topic',blog='msg').get(request.forms.typ),request.forms.topicid or nmsg, nmsg))

@post('/u/point')
def create_message_point():
    ud = udata(request.forms.pauth.encode('utf-8'))
    dta = b64d(request.forms.tmsg.encode('utf-8')).decode('utf-8').splitlines()
    repto, tags = '', ''
    if dta[4].startswith('@repto:'):
        repto = dta[4][7:]
        if len(repto) != 20:
            return 'wrong repto!'
        txt = '\n'.join(dta[5:])
    elif dta[4].startswith('@tags:'):
        tags = dta[4][6:]
        txt = '\n'.join(dta[5:])
    else:
        txt = '\n'.join(dta[4:])
    mo = mydict(ea=dta[0],txt=txt,repto=repto,tags=tags,to=dta[1],title=dta[2] or '***')
    if repto:
        mo.topicid = api.get_msg(repto).topicid
    if ud.check() and ud.uname:
        nmsg = api.create_msg(mo,ud)
    return 'msg ok:%s' % nmsg

@route('/sign/get-<f:re:pub-key|blacklist>')
def get_key(f):
    response.content_type='text/plain; charset=UTF-8'
    return open('keys/pub.key' if f == 'pub-key' else 'data/keysbk.txt').read()

@post('/user/testkey')
def key_test_api():
    if udata(request.forms.kvitok.encode('utf-8')).check():
        return 'ok'

@route('/admin',method=['GET','POST'])
def adm_in():
    if request.method=='POST':
        response.set_cookie('admikey', request.forms.admikey.encode('utf-8'), path='/', max_age=7776000)
        return template('<a href="/user/me?ea={{ea}}">admikey set</a>',ea=request.forms.ea)
    else:
        if ak():
            return template('<form method="post"><input type="hidden" name="ea" value="{{ea}}"><input type="submit" value="Снять полномочия администратора"> или <a href="/user/me?ea={{ea}}">нет</a></form>',ea=request.query.ea)
        else:
            return template('<form method="post"><input type="hidden" name="ea" value="{{ea}}"><input type="text" name="admikey" placeholder="admikey"><input type="submit" value="Ok"> | <a href="/user/me?ea={{ea}}">Отмена</a></form>',ea=request.query.ea)

@route('/admin/del',method=['GET','POST'])
def admin_del():
    if request.forms.admikey:
        if ak():
            if request.forms.msgid:
                lenin.del_all(request.forms.msgid.encode('utf-8'))
                return '<a href="/">ok</a>'
    else:
        return template('''<form method="post"><input type="hidden" name="admikey" value="{{admikey}}"><p><input type="checkbox" name="msgid" value="{{rq.msgid}}" checked="on"> удалить</p>
<!--                <p><input type="checkbox" name="delall" value="{{rq.addr}} {{rq.msgid}}"> удалить все сообщения пользователя {{rq.who}} ({{rq.addr}}</p>
                <p><input type="checkbox" name="ban" value="1"> ... и заблокировать написание им сообщений</p>
                <p><input type="checkbox" name="dl" value="1"> заблеклистить указанные сообщение (нужно только при обмене, чтобы не получить их снова)</p> -->
                <p><input type="submit" value="Ok"></p></form>''', rq=request.query,admikey=request.cookies.admikey)


@post('/user/me')
def user_login():
    up = request.forms.upass1.strip().encode('utf-8')
    out = reg.mk_reg(request.forms)
    if up.startswith(':') and up.endswith(':'):
        ud = udata(up)
    else:
        if not out.startswith(':'):
            return out
        ud = udata(out)
    response.set_cookie('kvitok', ud.kvitok.encode('utf-8'), path='/', max_age=7776000)
    return template('reg/user.html',u=ud,ea=request.forms.ea,admikey=ak())

@route('/user/me')
def user_info():
    ud = u()
    if request.query.logout:
        response.set_cookie('kvitok', '', path='/', max_age=7776000)
        ud = udata('')
    return template('reg/user.html',u=ud,ea=request.query.ea,admikey=ak())

@route('/user/login')
def user_info():
    return template('reg/frmlogin.html',u=u(),ea=request.query.ea)

@route('/user/register')
def user_info():
    return template('reg/frmuadd.html',u=u(),ea=request.query.ea)

@route('/rss/<req>/<tid>')
def out_rss(req,tid):
    response.set_header('content-type','application/rss+xml; charset=utf-8')
    if req == 'topic':
        return rss.gen_topic(tid)
    elif req == 'msgs':
        return rss.gen_blog(tid)
    else:
        return rss.gen_all(tid)

@route('/s/<f:path>')
def send_file(f):
    return static_file(f, root='./s')


run(host='0.0.0.0',port=13014,debug=True)
