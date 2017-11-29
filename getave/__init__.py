import random, zlib

def aa32_fn(s):
    return s.replace(' ','_').replace('*','_').replace('[','_').replace(']','_').replace('\'','').replace('/','_')

ave32 = [(aa32_fn(x), x) for x in open('getave/getave32').read().splitlines()]

def aa32(newseed):
    # +2147483648 for hash result
    random.seed(newseed)
    out = random.choice(ave32)[0]
    random.seed()
    return out

def aa32raw(s):
    newseed = zlib.crc32(s,0)
    return aa32(newseed)