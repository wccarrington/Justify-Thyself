import os
import texture

textures = {}

def dircontents(dir):
    ret = []
    walker = os.walk(dir)
    l = len(dir)+1
    for x in walker:
        ret += [(i, x[0] + '/' + i) for i in x[2]]
    return ret

def loadtexture(name):
    if name not in textures:
        dircon = dict(dircontents('art'))
        try:
            textures[name] = texture.Texture(dircon[name])
        except KeyError:
            textures[name] = texture.Texture(name)
    return textures[name]
