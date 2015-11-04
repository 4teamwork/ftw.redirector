from zope.interface import Interface


class IRedirectorLayer(Interface):
    """Request layer interface for when ftw.redirector.
    """


class IRedirectConfig(Interface):
    """This interface is provided by the redirect config object.
    The interface can also be used to lookup the config by adapting
    any acquisition wrapped object with it.
    """


class IRedirectStrategy(Interface):
    """The redirect strategy finds a redirect target for the current request.
    """

    def __init__(config, request):
        """Multi adapter, adapting the redirect config and the request.
        """

    def find_redirect(path):
        """Finds a redirect in the adapted redirect config for ``path``.
        If there is an appropriate redirect, the target path is returned.
        If there is no redirect, None is returned.

        The input as well as the output path is considered to be relative
        to the Plone site root and start with a slash.
        """
