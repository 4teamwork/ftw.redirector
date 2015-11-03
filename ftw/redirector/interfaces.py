from zope.interface import Interface


class IRedirectorLayer(Interface):
    """Request layer interface for when ftw.redirector.
    """


class IRedirectConfig(Interface):
    """This interface is provided by the redirect config object.
    The interface can also be used to lookup the config by adapting
    any acquisition wrapped object with it.
    """
