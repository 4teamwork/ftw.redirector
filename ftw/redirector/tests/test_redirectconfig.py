from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase


class TestRedirectConfig(FunctionalTestCase):

    def test_getting_redirectconfig_by_adapting_context(self):
        config = IRedirectConfig(self.layer['portal'])
        self.assertTrue(IRedirectConfig.providedBy(config))

    def test_config_title(self):
        config = IRedirectConfig(self.layer['portal'])
        self.assertEquals('Redirect Configuration',
                          config.Title())
