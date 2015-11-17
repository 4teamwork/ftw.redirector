from ftw.redirector.excel import create_rules_excel
from Products.Archetypes.utils import contentDispositionHeader
from Products.Five.browser import BrowserView


class ExportRedirectConfigView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        response = self.request.RESPONSE
        filename = "redirector_config.xlsx"

        disp = contentDispositionHeader('attachment', 'l1', filename=filename)
        response.setHeader("Content-Disposition", disp)
        response.setHeader("Content-Type", 'application/vnd.ms-excel')

        return create_rules_excel()
