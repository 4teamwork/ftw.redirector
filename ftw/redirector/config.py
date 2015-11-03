from Acquisition import aq_inner
from Acquisition import aq_parent
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


REDIRECT_CONFIG_ID = 'redirect-config'


class IRedirectConfigSchema(form.Schema):
    pass


alsoProvides(IRedirectConfigSchema, IFormFieldProvider)


class RedirectConfig(Item):
    implements(IRedirectConfig)

    def Title(self):
        return 'Redirect Configuration'


@adapter(IContentish)
@implementer(IRedirectConfig)
def lookup_config(context):
    return aq_parent(aq_inner(context))


@adapter(IPloneSiteRoot)
@implementer(IRedirectConfig)
def lookup_config_on_portal(portal):
    return portal.get(REDIRECT_CONFIG_ID)
