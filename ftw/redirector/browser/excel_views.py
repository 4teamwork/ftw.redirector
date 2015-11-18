from ftw.redirector import _
from ftw.redirector.config import RulesValidator
from ftw.redirector.excel import create_rules_excel
from ftw.redirector.excel import load_rules_from_excel
from ftw.redirector.excel import RULES_START_ROW
from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.interfaces import IRedirectorLayer
from plone.directives import form
from plone.formwidget.namedfile.widget import NamedFileWidget
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.interfaces import INamedFileField
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from z3c.form import button
from z3c.form.interfaces import IFieldWidget
from z3c.form.validator import WidgetValidatorDiscriminators
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.component import provideAdapter
from zope.interface import implementer
from zope.interface import Invalid


class ExportRedirectConfigView(BrowserView):

    def __call__(self):
        response = self.request.RESPONSE
        filename = "redirector_config.xlsx"

        response.setHeader('Content-Disposition',
                           'attachment; filename={}'.format(filename))
        response.setHeader("Content-Type", 'application/vnd.ms-excel')

        return create_rules_excel()


class RedirectConfigExcelValidator(RulesValidator):

    def validate(self, value):
        if not value:
            raise Invalid(_(u'missing_input_data',
                            default=u'Please upload a rules excel file.'))
        excel_file = StringIO(value.data)
        rules = load_rules_from_excel(excel_file)
        map(self.validate_row, enumerate(rules, RULES_START_ROW))


class ForceFileUploadWidget(NamedFileWidget):
    allow_nochange = False


@implementer(IFieldWidget)
@adapter(INamedFileField, IRedirectorLayer)
def ForceFileUploadFieldWidget(field, request):
    return FieldWidget(field, ForceFileUploadWidget(request))


class IRulesUploadSchema(form.Schema):
    form.primary('rules_file')
    rules_file = NamedBlobFile(
        title=_(u'redirect_config_file',
                default=u'Excel redirect config'),
        required=True)


WidgetValidatorDiscriminators(RedirectConfigExcelValidator,
                              field=IRulesUploadSchema['rules_file'])
provideAdapter(RedirectConfigExcelValidator)


class ImportRedirectConfigView(form.SchemaForm):

    schema = IRulesUploadSchema
    ignoreContext = True

    label = _(u"Upload redirect config")

    def updateWidgets(self):
        # use the basic widget to disable "keep existing file"
        self.fields['rules_file'].widgetFactory = ForceFileUploadFieldWidget
        super(ImportRedirectConfigView, self).updateWidgets()

    @button.buttonAndHandler(u'Upload')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            # since we have only one field we can copy the error message
            # to make it more visible
            self.status = errors[0].message
            return

        excel_file = StringIO(data['rules_file'].data)
        rules = load_rules_from_excel(excel_file)

        rconfig = IRedirectConfig(self.context)
        rconfig.rules = rules

        messages = IStatusMessage(self.request)
        messages.add(_("The redirect config has been replaced."), type=u'info')

        self.request.RESPONSE.redirect(self.context.absolute_url())
