from ftw.redirector.interfaces import IRedirectorLayer
from ftw.redirector.tests import FunctionalTestCase
from plone.browserlayer.utils import registered_layers
from Products.CMFCore.utils import getToolByName


class TestInstallation(FunctionalTestCase):

    def test_profile_installed(self):
        portal = self.layer['portal']
        portal_setup = getToolByName(portal, 'portal_setup')

        version = portal_setup.getLastVersionForProfile(
            'ftw.redirector:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')

    def test_request_layer_active(self):
        layers = registered_layers()
        self.assertIn(IRedirectorLayer, layers)
