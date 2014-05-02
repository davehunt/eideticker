# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait

from eideticker.test import B2GAppStartupTest


class Test(B2GAppStartupTest):
    def __init__(self, testinfo, appname, **kwargs):
        B2GAppStartupTest.__init__(self, testinfo, appname, **kwargs)

    def wait_for_content_ready(self):
        Wait(self.marionette).until(lambda m: m.execute_script(
            'return window.wrappedJSObject.Browser.hasLoaded;'))
