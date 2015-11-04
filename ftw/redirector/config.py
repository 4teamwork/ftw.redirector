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
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import implements
from zope.schema import List
from zope.schema import TextLine


REDIRECT_CONFIG_ID = 'redirect-config'


class IRule(form.Schema):

    source_path = TextLine(
        title=_(u'label_source_path', default=u'Source Path'))

    destination_path = TextLine(
        title=_(u'label_destination_path', default=u'Destination Path'))


class IRedirectConfigSchema(form.Schema):

    form.widget('rules', DataGridFieldFactory)
    rules = List(
        title=_(u'label_redirect_rules', default=u'Redirect rules'),
        value_type=DictRow(schema=IRule))


alsoProvides(IRedirectConfigSchema, IFormFieldProvider)


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
    return aq_parent(aq_inner(context))


@adapter(IPloneSiteRoot)
@implementer(IRedirectConfig)
def lookup_config_on_portal(portal):
    return portal.get(REDIRECT_CONFIG_ID)
