# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.camera.app import Camera
from gaiatest.gaia_test import GaiaApps

from eideticker.test import B2GAppStartupTest


class Test(B2GAppStartupTest):

    def prepare_app(self):
        apps = GaiaApps(self.device.marionette)
        apps.set_permission('Camera', 'geolocation', 'deny')

    def wait_for_content_ready(self):
        app = Camera(self.device.marionette)
        app.wait_for_capture_ready()
