from ftw.redirector.excel import create_rules_excel
from ftw.redirector.excel import load_rules_from_excel
from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from openpyxl import load_workbook
from StringIO import StringIO
import os


class TestRedirectConfigExportImport(FunctionalTestCase):

    @browsing
    def test_excel_actions_are_available(self, browser):
        self.grant('Manager')
        browser.login().open(IRedirectConfig(self.portal))
        self.assertIn("Excel export", browser.contents)
        self.assertIn("Excel import", browser.contents)

    @browsing
    def test_excel_views_are_available(self, browser):
        self.grant('Manager')
        browser.login()
        browser.open(IRedirectConfig(self.portal), view='import')
        browser.open(IRedirectConfig(self.portal), view='export')

    @browsing
    def test_export(self, browser):
        self.grant('Manager')
        browser.login().open(IRedirectConfig(self.portal))
        browser.find(u'Edit').click()
        browser.fill(
            {u'Redirect rules': [
                {u'Source Path': u'/foo',
                 u'Destination': u'/bar'},
                {u'Source Path': u'/something/one',
                 u'Destination': u'/something/two'}]}).save()

        excel_file = StringIO(create_rules_excel())
        excel = load_workbook(excel_file)
        sheet = excel.active

        self.assertEquals('/foo', sheet['A2'].value)
        self.assertEquals('/something/one', sheet['A3'].value)
        self.assertEquals('/bar', sheet['B2'].value)
        self.assertEquals('/something/two', sheet['B3'].value)

    def test_load_rules_from_excel(self):
        file_data = open("%s/assets/redirector_config_invalid.xlsx" % os.path.split(__file__)[0], 'r')
        rules = load_rules_from_excel(file_data)

        self.assertEquals(
            [{'destination': u'/Plone', 'source_path': u'/theploneasdf'},
             {'destination': u'http://www.google.ch/', 'source_path': u'/google'},
             {'destination': u'/ziel', 'source_path': u'/test'},
             {'destination': '', 'source_path': u'/bla'},
             {'destination': u'/gnarg', 'source_path': ''},
             {'destination': u'/same', 'source_path': u'/same'}],
            rules
        )

    @browsing
    def test_import(self, browser):
        file_data = open("%s/assets/redirector_config.xlsx" % os.path.split(__file__)[0], 'r')
        file_ = StringIO(file_data.read())
        file_.filename = 'redirector_config.xlsx'
        file_.content_type = 'application/vnd.ms-excel'

        self.grant('Manager')
        browser.login().open(IRedirectConfig(self.portal), view='import')
        browser.fill({'Excel redirect config': file_}).submit()

        self.assertEquals(
            [{'destination': u'/Plone', 'source_path': u'/theploneasdf'},
             {'destination': u'http://www.google.ch/', 'source_path': u'/google'},
             {'destination': u'/ziel', 'source_path': u'/test'},
             {'destination': u'/blub', 'source_path': u'/bla'},
             {'destination': u'/gnarg', 'source_path': u'/gna'},
             {'destination': u'/same', 'source_path': u'/same'}],
            IRedirectConfig(self.portal).rules
        )
