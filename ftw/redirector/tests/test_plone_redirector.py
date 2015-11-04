from ftw.builder import Builder
from ftw.builder import create
from ftw.redirector.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import transaction


class TestPloneRedirector(FunctionalTestCase):

    @browsing
    def test_moved_objects_are_still_found(self, browser):
        """The default plone.app.redirector behavior
        should still work.
        """
        self.grant('Manager')

        source = create(Builder('folder').titled('Source'))
        target = create(Builder('folder').titled('Target'))
        page = create(Builder('page').titled('Page').within(source))

        browser.login().open(page)
        self.assertEquals('http://nohost/plone/source/page', browser.url)

        clipboard = source.manage_cutObjects(page.getId())
        target.manage_pasteObjects(clipboard)
        transaction.commit()

        browser.replace_request_header('X-zope-handle-errors', 'True')
        browser.open('http://nohost/plone/source/page')
        self.assertEqual('http://nohost/plone/target/page', browser.url)
