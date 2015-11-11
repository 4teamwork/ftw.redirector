from ftw.builder import Builder
from ftw.builder import create
from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from plone import api
import transaction


class TestRedirectConfig(FunctionalTestCase):

    def test_get_config_by_adapting_portal(self):
        config = IRedirectConfig(self.portal)
        self.assertTrue(IRedirectConfig.providedBy(config))

    def test_get_config_by_adapting_any_context_in_site_root(self):
        self.grant('Manager')
        obj = create(Builder('folder').within(create(Builder('folder'))))
        self.assertEquals(IRedirectConfig(self.portal), IRedirectConfig(obj))
        self.assertTrue(IRedirectConfig.providedBy(IRedirectConfig(obj)))

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
                 u'Destination': u'/bar'},
                {u'Source Path': u'/something/one',
                 u'Destination': u'/something/two'}]}).save()

        self.assertEquals( [{'destination': u'/bar',
                             'source_path': u'/foo'},
                            {'destination': u'/something/two',
                             'source_path': u'/something/one'}],
                           IRedirectConfig(self.portal).rules)

    @browsing
    def test_control_panel_action_points_to_config_object(self, browser):
        self.grant('Manager')
        browser.login().open(view='@@overview-controlpanel')
        browser.css('.configlets').find('Redirect Configuration').first.click()
        self.assertEquals('http://nohost/plone/redirect-config', browser.url)

    @browsing
    def test_control_panel_only_visible_when_config_visible(self, browser):
        user = create(Builder('user').with_roles('Site Administrator'))
        browser.login(user).open(view='@@overview-controlpanel')
        self.assertIn('Redirect Configuration',
                      browser.css('.configlets a').text)

        IRedirectConfig(self.portal).manage_permission('View', [], acquire=False)
        transaction.commit()
        browser.reload()
        self.assertNotIn('Redirect Configuration',
                         browser.css('.configlets a').text)
