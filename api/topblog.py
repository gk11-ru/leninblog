from api import lst, rf, get_ea
import os

def gettop(ea,cnt=6):
    if ea:
        ealist = set(get_ea(ea))
    topc = []
    for n in os.listdir('data/nuser'):
        un = rf('data/nuser/%s' % n)
        l = len([x for x in lst('carbon/_%s' % n) if not ea or (x in ealist)])
        if l:
            topc.append([l,un])
    return list(reversed(sorted(topc)))[:cnt]
