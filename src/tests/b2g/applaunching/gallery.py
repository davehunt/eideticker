import time

from gaiatest.apps.gallery.app import Gallery
from marionette import By
from marionette import Wait
from marionette import expected

from eideticker.test import B2GAppStartupTest


class Test(B2GAppStartupTest):
    picture_count = 100

    def prepare_app(self):
        self.device.b2gpopulate.populate_pictures(self.picture_count)
        app = Gallery(self.device.marionette)
        app.launch()
        # Bug 922608 - Wait for the gallery app to finish scanning
        time.sleep(5)
        self.wait_for_content_ready()

    def wait_for_content_ready(self):
        Wait(self.marionette, timeout=240).until(
            lambda m: len(m.find_elements(
                By.CSS_SELECTOR, '.thumbnail')) == self.picture_count)
        Wait(self.marionette, timeout=60).until(expected.element_not_displayed(
            self.marionette.find_element(*self.app._progress_bar_locator)))
