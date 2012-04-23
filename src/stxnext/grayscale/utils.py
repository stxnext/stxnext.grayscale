import re
from PIL import Image
from StringIO import StringIO

from stxnext.grayscale import log

COLOR_PATTERN = re.compile(r" aqua | black | blue | fuchsia |gray| green |"+\
                            " lime | maroon | navy | olive | orange |"+\
                            " purple | red | silver | teal | white | yellow |"+\
                            "#[a-f0-9]{6}|#[a-f0-9]{3}|"+\
                            "rgb\(.+\)", re.M | re.I)

#css color names and their grayscale versions in css notation.
KWRD_MAP = {
  'aqua': '#aaaaaa',
  'black': '#000000',
  'blue': '#555555',
  'fuchsia': '#aaaaaa',
  'gray': '#808080',
  'green': '#2a2a2a',
  'lime': '#55555',
  'maroon': '#2a2a2a',
  'navy': '#2a2a2a',
  'olive': '#555555',
  'orange': '#8c8c8c',
  'purple': '#555555',
  'red': '#555555',
  'silver': '#c0c0c0',
  'teal': '#555555',
  'white': '#ffffff',
  'yellow': '#aaaaaa'}


def avg_tuple(tup):
    """
    Takes a 3-tuple and returns a 3-tuple,
    with average of the input.
    """
    avg = (tup[0] + tup[1] + tup[2])/3
    return (avg, avg, avg)


def is_grey(tup):
    """
    Chekcs if givet tuple has equal elements
    """
    if len(tup) != 3: return False
    return len(set(tup)) == 1


def hex_to_tuple(text):
    """
    Transform #rrggbb notation of color 
    to 3-tuple (r, g, b)
    """
    text.strip()
    text = text.replace('#', '')
    if len(text) == 3:
        r, g, b = (text[0], text[1], text[2])
    elif len(text) == 6:
        r, g, b = (text[:2], text[2:4], text[4:])
    else:
        return text
    return tuple([int(x, 16) for x in (r, g, b)])


def rgb_to_tuple(text):
    """
    Transforms rgb(x,x,x) both in decimal and %
    notation of color to 3-tuple (r, g, b)
    """
    if '%' in text:
        rem = ('rgb', '(', ')', ',', ' ')
        for x in rem: text = text.replace(x, '')
        res = text.split('%')
        res = filter(None, res)
        return tuple([int((int(x)/100.0) * 255) for x in res])
    else:
        rem = ('rgb','(', ')', '%', ' ')
        for x in rem: text = text.replace(x, '')
        text = text.split(',')
        return tuple([int(x) for x in text])


def tuple_to_rgb(tup):
    """
    Transforms 3-tuple with colors to 
    #RRGGBB html notation.
    """
    return '#%02x%02x%02x' % tup


def transform_value(val):
    """
    Transforms a single color value to grayscale.
    """
    if val.lower() in KWRD_MAP:
        #colors as keywords
        val = KWRD_MAP[val.lower()]
    else:
        if val.startswith('#'):
            #colors as #rrggbb
            tup_val = hex_to_tuple(val)
        elif val.startswith('rgb'):
            #colors as rgb(x,y,z)
            tup_val = rgb_to_tuple(val)
        else:
	        return val
        if is_grey(tup_val): return val
        
        val= tuple_to_rgb(avg_tuple(tup_val))
    return val


def transform_sheet(sheetstr):
    """
    Accepts string. Transform single stylesheet to grayscale 
    using regexp.
    """
    #to do:
    # extract colors only from given attributes
    # handle shorhand properties
    matches = COLOR_PATTERN.findall(sheetstr)
    for match in set(matches):
        avg = transform_value(match)
        sheetstr = sheetstr.replace(match, avg)
    return sheetstr


def image_to_grayscale(image, path):
    """
    converts image data to grayscale using PIL library 
    """
    try:
        imagestring = StringIO(image)
        image_file = Image.open(imagestring)
        converted = image_file.convert('RGBA')
        converted = converted.convert('LA')
        res = StringIO()
        converted.save(res, format='PNG')
        return res.getvalue()
    except IOError, err:
        log.error('Error while transforming image: %s : %s' % (path, err))
        return image


def add_bodyclass(html_text):
    """
    applies the 'gray-scale' css class on body tag 
    """
    bodymatches = re.findall(r"<body.*>", html_text, re.I)
    for bodytag in bodymatches:
        if 'class' in bodytag:
            for css_classs in re.findall(r"class\s*=\s*[\'\"](.*)[\'\"]", bodytag, re.I):
                modified_bodytag = bodytag.replace(css_classs, ' '.join((css_classs, 'gray-style')))
        else:
            modified_bodytag = bodytag.replace('>', ' class="gray-style">')
        html_text = html_text.replace(bodytag, modified_bodytag)
    return html_text
