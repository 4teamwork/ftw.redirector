from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from plone import api


class TestRedirectConfig(FunctionalTestCase):

    def test_getting_redirectconfig_by_adapting_context(self):
        config = IRedirectConfig(self.layer['portal'])
        self.assertTrue(IRedirectConfig.providedBy(config))

    def test_config_title(self):
        config = IRedirectConfig(self.layer['portal'])
        self.assertEquals('Redirect Configuration',
                          config.Title())

    def test_excluded_from_navigation(self):
        config_brain, = api.content.find(portal_type='ftw.redirector.RedirectConfig')
        self.assertTrue(config_brain.exclude_from_nav,
                        'Should be excluded from navigation.')
