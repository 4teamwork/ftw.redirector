from ftw.builder import Builder
from ftw.builder import create
from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from ftw.redirector.tests.helpers import make_rules
from ftw.testbrowser import browsing


class TestRedirectingOnNotFound(FunctionalTestCase):

    @browsing
    def test_redirected_when_having_matching_rule(self, browser):
        self.grant('Manager')
        config = IRedirectConfig(self.portal)
        config.rules = make_rules(('/foo', '/target'))
        create(Builder('page').titled(u'target'))

        # Set accept header (needed since Plone 5).
        browser.append_request_header('Accept', 'text/html')

        browser.open('http://nohost/plone/foo')
        self.assertEqual('http://nohost/plone/target', browser.url)

    @browsing
    def test_no_redirect_when_object_exists_and_no_404_happens(self, browser):
        self.grant('Manager')
        config = IRedirectConfig(self.portal)
        config.rules = make_rules(('/foo', '/target'))
        create(Builder('page').titled(u'target'))

        # Set accept header (needed since Plone 5).
        browser.append_request_header('Accept', 'text/html')

        browser.open('http://nohost/plone/foo')
        self.assertEqual('http://nohost/plone/target', browser.url)

        create(Builder('page').titled(u'foo'))
        browser.open('http://nohost/plone/foo')
        self.assertEqual('http://nohost/plone/foo', browser.url)

    @browsing
    def test_redirecting_with_umlauts(self, browser):
        self.grant('Manager')
        config = IRedirectConfig(self.portal)
        config.rules = make_rules((u'/hall\xf6chen', u'/target'))
        create(Builder('page').titled(u'target'))

        # Set accept header (needed since Plone 5).
        browser.append_request_header('Accept', 'text/html')

        browser.open('http://nohost/plone/hall\xc3\xb6chen')
        self.assertEqual('http://nohost/plone/target', browser.url)
