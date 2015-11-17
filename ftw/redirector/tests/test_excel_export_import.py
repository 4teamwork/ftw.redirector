from ftw.redirector.excel import create_rules_excel
from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from openpyxl import load_workbook
from StringIO import StringIO


class TestRedirectConfigExportImport(FunctionalTestCase):

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

        self.assertEquals('/foo', sheet['A4'].value)
        self.assertEquals('/something/one', sheet['A5'].value)
        self.assertEquals('/bar', sheet['B4'].value)
        self.assertEquals('/something/two', sheet['B5'].value)
