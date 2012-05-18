import unittest

from stxnext.grayscale import utils


HEX_COLORS = """
border: 1px solid #fff;
border: 1pt solid #00FF00;
background: 123456;
background:#aaaaaa;
color:#1234;

style="color:#ff0"
"""
HEX_MATCH = sorted(['#fff', '#00FF00', '#aaaaaa', '#ff0'])

RGB_RGBA_COLORS = """
border: 1px solid rgb(10%, 20%, 10%);
border: 1pt solid rgba(11%,22%,33%, 0.1);
background: rgb(11,11);
background:rgba(44,55,66, 1);
color:rgb(44%,55%,66%);

style="color: rgb(1,2,3)"
"""
RGB_RGBA_MATCH = sorted(['rgb(10%, 20%, 10%)', 'rgba(11%,22%,33%, 0.1)',
    'rgb(11,11)', 'rgba(44,55,66, 1)', 'rgb(44%,55%,66%)', 'rgb(1,2,3)'])

NAMED_COLORS = """
border: 1px solid white; // will not be matched
border: 1pt solid black; // will not be matched
background-color: 123456;
color:       yellow;

style="color:red"
"""
NAMED_MATCH = sorted(['color:       yellow', 'color:red'])


class TestRegexpPatterns(unittest.TestCase):
    """
    Tests for regexp patterns
    """
    def test_match_hex_colors(self):
        """
        Tests COLOR_PATTERN for hex colors
        """
        colors = sorted(utils.COLOR_PATTERN.findall(HEX_COLORS))
        self.assertEqual(colors, HEX_MATCH)

    def test_match_rgb_rgba_colors(self):
        """
        Tests COLOR_PATTERN for RGB and RGBA colors
        """
        colors = sorted(utils.COLOR_PATTERN.findall(RGB_RGBA_COLORS))
        self.assertEqual(colors, RGB_RGBA_MATCH)

    def test_match_named_colors(self):
        """
        Tests COLOR_PATTERN for colors specified by name
        """
        colors = sorted(utils.COLOR_PATTERN.findall(NAMED_COLORS))
        self.assertEqual(colors, NAMED_MATCH)

    def test_dont_match_entities(self):
        """
        Tests if COLOR_PATTERN will not match HTML entities
        """
        entities = "&#60; &#160 &#182; &#8364; &#123456"
        self.assertFalse(utils.COLOR_PATTERN.findall(entities))



class TestAddParamToUrl(unittest.TestCase):
    """
    Test for stxnext.grayscale.utils.add_param_to_url function
    """

    def test_add_param_to_domain_wo_params(self):
        url_domain_only = 'http://example.com'
        self.assertEqual(utils.add_param_to_url(url_domain_only),
                'http://example.com?grayscale=1')

    def test_add_param_to_path_wo_params(self):
        url_with_path = 'http://example.com/abc/efg/'
        self.assertEqual(utils.add_param_to_url(url_with_path),
                'http://example.com/abc/efg/?grayscale=1')

    def test_add_param_to_file_wo_params(self):
        url_with_file = 'http://example.com/file.html'
        self.assertEqual(utils.add_param_to_url(url_with_file),
                'http://example.com/file.html?grayscale=1')

    def test_add_param_to_domain_w_params(self):
        url_domain_only = 'http://example.com?param1=2'
        self.assertEqual(utils.add_param_to_url(url_domain_only),
                'http://example.com?param1=2&grayscale=1')

    def test_add_param_to_path_w_params(self):
        url_with_path = 'http://example.com/abc/efg/?param1=2'
        self.assertEqual(utils.add_param_to_url(url_with_path),
                'http://example.com/abc/efg/?param1=2&grayscale=1')

    def test_add_param_to_file_w_params(self):
        url_with_file = 'http://example.com/file.html?param1=2'
        self.assertEqual(utils.add_param_to_url(url_with_file),
                'http://example.com/file.html?param1=2&grayscale=1')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
