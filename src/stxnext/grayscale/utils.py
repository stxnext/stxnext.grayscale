import re
from PIL import Image
from StringIO import StringIO

from stxnext.grayscale import log

COLOR_PATTERN = re.compile(r"#[a-fA-F0-9]{6}")

def htmls_color_to_rgb(colorstring):
    """
    converts #RRGGBB to an (R, G, B) tuple
    """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

def rgb_to_html_color(rgb_tuple):
    """
    converts an (R, G, B) tuple to #RRGGBB
    """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    return hexcolor

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
