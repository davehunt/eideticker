from eideticker.test import B2GAppStartupTest
from eideticker.b2gtestmixins import B2GSettingsTestMixin


class Test(B2GSettingsTestMixin, B2GAppStartupTest):

    def __init__(self, testinfo, appname, **kwargs):
        B2GAppStartupTest.__init__(self, testinfo, appname, **kwargs)
