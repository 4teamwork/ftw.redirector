from ftw.redirector import _
from ftw.redirector.interfaces import IRedirectConfig
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.writer.excel import save_virtual_workbook
from plone import api
from zope.i18n import translate


def create_rules_excel():
    portal = api.portal.get()
    request = portal.REQUEST

    rules = IRedirectConfig(portal).rules

    book = Workbook()
    sheet = book.active

    title = translate(_(u'Redirect Configuration'), context=request)
    source_title = translate(_(u'label_source_path',
                             default=u'Source Path'), context=request)
    destination_title = translate(_(u'label_destination',
                                  default=u'Destination'), context=request)

    # HEADER
    sheet.title = title

    bold = Font(bold=True)
    cell = sheet.cell(column=1, row=1)
    cell.font = bold
    cell.value = title

    cell = sheet.cell(column=1, row=3)
    cell.font = bold
    cell.value = source_title

    cell = sheet.cell(column=2, row=3)
    cell.font = bold
    cell.value = destination_title

    # DATA
    rules_start_index = 4

    for rule_nr, rule in enumerate(rules):
        cell = sheet.cell(column=1, row=rules_start_index+rule_nr)
        cell.value = rule['source_path']
        cell = sheet.cell(column=2, row=rules_start_index+rule_nr)
        cell.value = rule['destination']

    # match the width to the longest entry
    for column in sheet.columns:
        maxwidth = 0
        for cell in column:
            if not cell.value:
                continue
            cwidth = len(cell.value)
            maxwidth = cwidth if cwidth > maxwidth else maxwidth
        # a bit more space for readability
        sheet.column_dimensions[cell.column].width = maxwidth + 5

    return save_virtual_workbook(book)


def import_rules_from_excel(excel):
    pass
