# -*- coding: utf-8 -*-

BRAND=u'blog.51t.ru'
TAGLINE=u'Старая школа'
EA='lenin.blog'
ADDR='lenina'
URL='http://blog.51.ru'
DESC=u'Проект развития блога для ELP предполагает различные представления. blog.51t.ru это эксперимент по созданию более функционального блога, чем в базовой поставке'

f = ''

def reload_cfg():
    global f, BRAND, TAGLINE, EA, ADDR, URL, DESC
    f = open('data/config').read().decode('utf-8').splitlines()
    if f:
        BRAND = f[0]
        TAGLINE = f[1]
        EA = f[2]
        ADDR = f[3]
        URL =f [4]
        DESC = f[5]

reload_cfg()