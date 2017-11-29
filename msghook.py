blacklist = set(open('data/blacklist.txt').read().splitlines())

def hook(o,newflag):
    if not newflag:
        if o.msgid in blacklist:
            return
    return o
