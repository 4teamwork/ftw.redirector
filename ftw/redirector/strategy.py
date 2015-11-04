from ftw.redirector.interfaces import IRedirectConfig
from ftw.redirector.interfaces import IRedirectStrategy
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
import re


class RedirectStrategy(object):
    adapts(IRedirectConfig, Interface)
    implements(IRedirectStrategy)

    def __init__(self, config, request):
        self.config = config

    def find_redirect(self, path):
        for redirect in self.config.rules or ():
            target = self._match(redirect, path)
            if target:
                return target
        return None

    def _match(self, redirect, path):
        path = beginning_slash(path)
        src = beginning_slash(redirect['source_path'])
        dst = beginning_slash(redirect['destination'])

        if ending_slash(path) == ending_slash(src):
            return dst

        if path.startswith(src):
            return re.sub('^{}/'.format(re.escape(src)),
                          ending_slash(dst),
                          path)

        return None


def beginning_slash(path):
    """Ensure slash on beginning of path.
    """
    if '://' in path:
        return path

    return '/' + path.lstrip('/')


def ending_slash(path):
    """Ensure slash on end of path.
    """
    return path.rstrip('/') + '/'
