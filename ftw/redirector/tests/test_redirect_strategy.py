from ftw.redirector.interfaces import IRedirectStrategy
from ftw.redirector.strategy import RedirectStrategy
from ftw.redirector.tests.helpers import make_rules
from unittest2 import TestCase
from zope.interface.verify import verifyClass


class Stub(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def named(self, name):
        self.__name__ = name
        return self


class TestRedirectStrategy(TestCase):

    def setUp(self):
        self.config = Stub(rules=[]).named('RedirectConfig')
        self.request = Stub().named('request')
        self.strategy = RedirectStrategy(self.config, self.request)

    def test_implements_interface(self):
        verifyClass(IRedirectStrategy, RedirectStrategy)

    def test_returns_None_when_no_redirects_configured(self):
        self.assert_redirect(None, '/missing')

    def test_no_trailing_slash(self):
        self.configure_redirects(('/missing', '/target'))
        self.assert_redirect('/target', '/missing')

    def test_trailing_slash_on_input_matches(self):
        self.configure_redirects(('/missing', '/target'))
        self.assert_redirect('/target', '/missing/')

    def test_no_match_for_similarily_starting_redirect(self):
        self.configure_redirects(('/fooing', '/bar'))
        self.assert_redirect(None, '/foo')

    def test_trailing_slash_added_when_in_config(self):
        self.configure_redirects(('/missing', '/target/'))
        self.assert_redirect('/target/', '/missing')

    def test_redirect_keeps_rest_path_without_slash_configured(self):
        self.configure_redirects(('/missing', '/target'))
        self.assert_redirect('/target/foo/bar', '/missing/foo/bar')

    def test_redirect_keeps_rest_path_with_slash_configured(self):
        self.configure_redirects(('/missing', '/target/'))
        self.assert_redirect('/target/foo/bar', '/missing/foo/bar')

    def test_redirects_are_applied_in_order_of_appearance(self):
        self.configure_redirects(('/foo', '/target1'),
                                 ('/foo/bar', '/target2'))
        self.assert_redirect('/target1', '/foo')
        self.assert_redirect('/target1/bar', '/foo/bar')

        self.configure_redirects(('/foo/bar', '/target2'),
                                 ('/foo', '/target1'))
        self.assert_redirect('/target1', '/foo')
        self.assert_redirect('/target2', '/foo/bar')

    def test_redirect_to_external_page(self):
        self.configure_redirects(('/google', 'https://google.com'))
        self.assert_redirect('https://google.com', '/google')
        self.assert_redirect('https://google.com/apps', '/google/apps')

    def assert_redirect(self, target, source, msg=None):
        self.assertEquals(target, self.strategy.find_redirect(source), msg=msg)

    def configure_redirects(self, *redirects):
        self.config.rules = make_rules(*redirects)
