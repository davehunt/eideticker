from gaiatest.gaia_test import GaiaApps

from eideticker.test import B2GAppStartupTest


class Test(B2GAppStartupTest):

    def prepare_app(self):
        apps = GaiaApps(self.device.marionette)
        apps.set_permission('Camera', 'geolocation', 'deny')
