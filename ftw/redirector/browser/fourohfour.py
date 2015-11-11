from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.interfaces import IRedirectStrategy
from plone import api
from plone.app.redirector.browser import FourOhFourView
from zope.component import getMultiAdapter
import os.path


class CustomFourOhFourView(FourOhFourView):

    def attempt_redirect(self):
        if not self.try_redirect():
            return super(CustomFourOhFourView, self).attempt_redirect()

    def try_redirect(self):
        path = self.get_path()
        if not path:
            return None

        config = IRedirectConfig(self.context, None)
        if not config:
            return None

        strategy = getMultiAdapter((config, self.request), IRedirectStrategy)
        target = strategy.find_redirect(path.decode('utf-8'))
        if not target:
            return None

        if '://' not in target:
            target = api.portal.get().absolute_url() + target
        return self.request.response.redirect(target, status=301, lock=1)

    def get_path(self):
        url = self._url()
        if not url:
            return None

        try:
            partials = self.request.physicalPathFromURL(url)
        except ValueError:
            return None

        path = '/'.join(partials)
        portal_path = '/'.join(api.portal.get().getPhysicalPath())
        return '/' + os.path.relpath(path, portal_path)
