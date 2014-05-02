from eideticker.test import B2GAppStartupTest
from eideticker.b2gtestmixins import B2GMessagesMixin


class Test(B2GMessagesMixin, B2GAppStartupTest):
    pass
