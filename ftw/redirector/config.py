from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from ftw.redirector import _
from ftw.redirector.interfaces import IRedirectConfig
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item
from plone.directives import form
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from z3c.form.validator import SimpleFieldValidator
from z3c.form.validator import WidgetValidatorDiscriminators
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import implements
from zope.interface import Invalid
from zope.schema import List
from zope.schema import TextLine
import re


REDIRECT_CONFIG_ID = 'redirect-config'


class IRule(form.Schema):

    source_path = TextLine(
        title=_(u'label_source_path', default=u'Source Path'))

    destination = TextLine(
        title=_(u'label_destination', default=u'Destination'))


class IRedirectConfigSchema(form.Schema):

    form.widget('rules', DataGridFieldFactory, allow_reorder=True)
    rules = List(
        title=_(u'label_redirect_rules', default=u'Redirect rules'),
        value_type=DictRow(schema=IRule),
    )


alsoProvides(IRedirectConfigSchema, IFormFieldProvider)


class RulesValidator(SimpleFieldValidator):

    def validate(self, value):
        map(self.validate_row, enumerate(value, 1))

    def validate_row(self, value):
        rownum, row = value
        self.validate_source_path(rownum, row['source_path'])
        self.validate_destination(rownum, row['destination'])

    def validate_source_path(self, rownum, value):
        if not value:
            raise Invalid(
                _(u'source_path_required',
                  default=u'Row ${rownum}: source path required.',
                  mapping={'rownum': rownum}))

        if value == '/':
            raise Invalid(
                _(u'source_path_invalid_root',
                  default=u'Row ${rownum}: invalid source path: cannot'
                  u' redirect from root.',
                  mapping={'rownum': rownum}))

        if value.startswith('/'):
            return

        raise Invalid(
            _(u'source_path_must_start_with_slash',
              default=u'Row ${rownum}: the source path "${value}"'
              u' must start with a slash.',
              mapping={'rownum': rownum, 'value': value}))

    def validate_destination(self, rownum, value):
        if not value:
            raise Invalid(
                _(u'destination_required',
                  default=u'Row ${rownum}: destination required.',
                  mapping={'rownum': rownum}))

        if value.startswith('/'):
            return

        if re.match(r'^https?://', value):
            return

        raise Invalid(
            _(u'destination_must_be_path_or_url',
              default=u'Row ${rownum}: the destination "${value}"'
              u' must be a path (start with slash)'
              u' or a full qualified URL.',
              mapping={'rownum': rownum, 'value': value}))


WidgetValidatorDiscriminators(RulesValidator,
                              field=IRedirectConfigSchema['rules'])


class RedirectConfig(Item):
    implements(IRedirectConfig)

    def Title(self):
        return _(u'Redirect Configuration')

    @property
    def exclude_from_nav(self):
        return True


@adapter(IContentish)
@implementer(IRedirectConfig)
def lookup_config(context):
    return IRedirectConfig(aq_parent(aq_inner(context)))


@adapter(IPloneSiteRoot)
@implementer(IRedirectConfig)
def lookup_config_on_portal(portal):
    return portal.get(REDIRECT_CONFIG_ID)
