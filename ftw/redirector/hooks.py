from plone.dexterity.utils import createContentInContainer
from plone import api
from ftw.redirector.config import REDIRECT_CONFIG_ID


def installed(portal):
    createContentInContainer(portal,
                             'ftw.redirector.RedirectConfig',
                             checkConstraints=False,
                             id=REDIRECT_CONFIG_ID)


def uninstalled(portal):
    if REDIRECT_CONFIG_ID in portal.objectIds():
        portal.manage_delObjects([REDIRECT_CONFIG_ID])

    controlpanel = api.portal.get_tool('portal_controlpanel')
    controlpanel.unregisterConfiglet('ftw.redirector')
