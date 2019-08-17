"""
Propagates kerning from the default master other members of a designspace
"""

from fontparts.world import OpenFont
import os

# MATH HELPERS

def lerp(start, stop, amt):
	"""
	Return the interpolation factor (between 0 and 1) of a VALUE between START and STOP.
	https://processing.org/reference/lerp_.html
	"""
	return float(amt-start) / float(stop-start)
	
def norm(value, start, stop):
	"""
	Interpolate using a value between 0 and 1
	See also: https://processing.org/reference/norm_.html
	"""
	return start + (stop-start) * value



# get point indexes from glyph
def getValueFromGlyphIndex(g, index):
    """
    Given a glyph and a point index, return that point.
    """
    index = int(index)
    i = 0
    for c in g:
        for p in c.points:
            if i == index:
                return (p.x, p.y)
            i += 1


# since we are not propagating to all sources, this is currently hard-coded

defaultPath = 'Amstelvar-Roman.ufo'

paths = [
    'Amstelvar-Roman-opsz-36.ufo', 
    'Amstelvar-Roman-opsz-84-wghtmin.ufo', 
    'Amstelvar-Roman-opsz-84.ufo', 
    'Amstelvar-Roman-opsz-max-wdthmin-wghtmax.ufo', 
    'Amstelvar-Roman-opsz-max-wghtmin.ufo', 
    'Amstelvar-Roman-opsz-max.ufo', 
    'Amstelvar-Roman-opsz-min.ufo', 
    'Amstelvar-Roman-wdthmax.ufo', 
    'Amstelvar-Roman-wdthmin.ufo', 
    'Amstelvar-Roman-wghtmax.ufo', 
    'Amstelvar-Roman-wghtmin.ufo'
]


default = OpenFont(os.path.join(os.getcwd(), defaultPath), showUI=False)
defaultxtraValue = getValueFromGlyphIndex(default['H'], 22)[0] - getValueFromGlyphIndex(default['H'], 11)[0]

print('default', defaultxtraValue)

for path in paths:
    f = OpenFont(os.path.join(os.getcwd(), path), showInterface=False)
    xtraValue = getValueFromGlyphIndex(f['H'], 22)[0] - getValueFromGlyphIndex(f['H'], 11)[0]
    m = xtraValue / defaultxtraValue
    print(path, m, xtraValue)
    
    f.groups.clear()
    f.kerning.clear()
    for groupName, groupGlyphs in default.groups.items():
        f.groups[groupName] = groupGlyphs

    f.kerning.update(default.kerning.asDict())
    for pair in f.kerning:
        value = f.kerning[pair]
        f.kerning[pair] = int(round(value * m))
    f.save()
print('done')