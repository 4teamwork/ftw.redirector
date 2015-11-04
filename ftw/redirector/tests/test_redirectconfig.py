from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone import api


class TestRedirectConfig(FunctionalTestCase):

    def test_getting_redirectconfig_by_adapting_context(self):
        config = IRedirectConfig(self.portal)
        self.assertTrue(IRedirectConfig.providedBy(config))

    def test_config_title(self):
        config = IRedirectConfig(self.portal)
        self.assertEquals('Redirect Configuration',
                          config.Title())

    def test_excluded_from_navigation(self):
        config_brain, = api.content.find(portal_type='ftw.redirector.RedirectConfig')
        self.assertTrue(config_brain.exclude_from_nav,
                        'Should be excluded from navigation.')

    @browsing
    def test_edit_configuration(self, browser):
        self.grant('Manager')
        browser.login().open(IRedirectConfig(self.portal))
        browser.find(u'Edit').click()
        browser.fill(
            {u'Redirect rules': [
                {u'Source Path': u'/foo',
                 u'Destination Path': u'/bar'},
                {u'Source Path': u'/something/one',
                 u'Destination Path': u'/something/two'}]}).save()

        self.assertEquals( [{'destination_path': u'/bar',
                             'source_path': u'/foo'},
                            {'destination_path': u'/something/two',
                             'source_path': u'/something/one'}],
                           IRedirectConfig(self.portal).rules)

    @browsing
    def test_control_panel_action_points_to_config_object(self, browser):
        self.grant('Manager')
        browser.login().open(view='@@overview-controlpanel')
        browser.css('.configlets').find('Redirect Configuration').first.click()
        self.assertEquals('http://nohost/plone/redirect-config', browser.url)
