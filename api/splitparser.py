# -*- coding: utf-8 -*-

import api.bottle as bottle, re

def sp(s,image):
    pre = 0; code = 0; txt = ''
    for n in s.splitlines():
        if n == '====' and pre == 0:
            txt += u'</p>====<pre>'
            pre = 1
        elif n == '====' and pre == 1:
            if code == 1: txt += '</code>'
            txt += u'</pre>====<p>\n'
            pre = 0; code = 0
        elif pre == 1:
            txt += u'%s\n' % n
        else:
            txt += u'%s\n' % _ac(n,image)
    if code == 1: txt += '</code>'
    if pre == 1: txt += '</pre>'
    return txt

def _ac(t,image):
    o = t
    if image and t.startswith('@image: '):
        return '<img class="%s" style="max-width:100%%" src="%s">' % (image, bottle.html_escape(t[8:]))
    else:
        if 'http://' in o:
            o = _btn(o,'http://')
        if 'https://' in o:
            o = _btn(o,'https://')
        if o.rstrip().startswith('&gt;'):
            o = u'<em style="color:green">%s</em>' % o
    return o

def _settag(s,tag):
    if tag == 'http://' or tag == 'https://':
#        if not '/' in s.rstrip('/'):
#            s = s.rstrip('/')
        return u'<a href="%s%s">%s</a>' % (tag,s,s)

def _btn(s,tag):
    k = s.split(tag)
    buf = k[0]
    for x in k[1:]:
        endl = x.split(' ',1)
        xl = None
        for eol in ('.',',',':','(',')','&quot;','&#039;', '&lt;', '&gt;'):
            if endl[0].endswith(eol):
                xl = _settag(endl[0][:-len(eol)],tag) + eol + ' ' + ' '.join(endl[1:])
        if xl is None: xl = _settag(endl[0],tag) + ' ' + ' '.join(endl[1:])
        buf += xl
    return buf

def rend(txt):
    out = bottle.html_escape(txt)
    out = sp(out)
    return out.replace('\n', '<br />')
