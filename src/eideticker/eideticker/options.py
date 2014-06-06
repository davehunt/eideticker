# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from device import getDevice, getDevicePrefs
from test import SRC_DIR
import json
import optparse
import os
import videocapture

GECKO_PROFILER_ADDON_DIR = os.path.join(SRC_DIR, "../src/GeckoProfilerAddon")

class OptionParser(optparse.OptionParser):
    '''Custom version of the optionparser class with a few eideticker-specific
       parameters to set device information'''

    def _add_options(self):
        self.add_option("--host", action="store",
                        type="string", dest="host",
                        help="Device hostname (only if using TCP/IP)",
                        default=None)
        self.add_option("-p", "--port", action="store",
                        type="int", dest="port",
                        help="Custom device port (if using SUTAgent or "
                        "adb-over-tcp)", default=None)
        self.add_option("-m", "--dm-type", action="store",
                        type="string", dest="dmtype",
                        default=os.environ.get('DM_TRANS', 'adb'),
                        help="DeviceManager type (adb or sut, defaults to "
                        "adb)")
        self.add_option("-d", "--device-type", action="store",
                        type="string", dest="devicetype",
                        default=os.environ.get('DEVICE_TYPE', 'android'),
                        help="Device type (android or b2g, default to "
                        "android). If B2G, you do not need to pass in an "
                        "appname")
        self.add_option("-w", "--wifi-settings", action="store",
                        type="string", dest="wifi_settings_file",
                        help="WIFI settings file (required for b2g)")
        self.add_option("--debug", action="store_true",
                        dest="debug", help="show verbose debugging "
                        "information")

    def __init__(self, **kwargs):
        optparse.OptionParser.__init__(self, **kwargs)
        self._add_options()


class CaptureOptionParser(OptionParser, videocapture.OptionParser):
    '''Custom version of the optionparser with eideticker-specific parameters
    to set device information + video capture related settings'''

    def __init__(self, **kwargs):
        videocapture.OptionParser.__init__(self, **kwargs)
        OptionParser._add_options(self)

    def parse_args(self):
        return videocapture.OptionParser.parse_args(self)


class TestOptionParser(CaptureOptionParser):
    '''Custom version of the optionparser with eideticker-specific parameters
    to set device information, video capture settings, and test-specific
    settings'''

    def __init__(self, **kwargs):
        CaptureOptionParser.__init__(self, **kwargs)

        self.add_option("--no-sync-time", action="store_false",
                        dest="sync_time",
                        help="don't synchronize time before running test",
                        default=True)
        self.add_option("--no-prepare-test", action="store_false",
                        dest="prepare_test",
                        help="don't prepare test (e.g. repopulate databases "
                        "for B2G)",
                        default=True)
        self.add_option("--extra-env-vars", action="store",
                        dest="extra_env_vars", default="",
                        help='Extra environment variables to set in '
                        '"VAR1=VAL1 VAR2=VAL2" format')
        self.add_option("--extra-prefs", action="store", dest="extra_prefs",
                        default="{}",
                        help="Extra profile preference for Firefox browsers. "
                        "Must be passed in as a JSON dictionary")
        self.add_option("--get-internal-checkerboard-stats",
                        action="store_true",
                        dest="log_checkerboard_stats",
                        help="get and calculate internal checkerboard stats (Android only)")
        self.add_option("--no-capture", action="store_false",
                        dest="capture", default=True,
                        help="Skip video capture (mainly for debugging)")
        self.add_option("--vpxenc", action="store_true",
                        dest="use_vpxenc", help="Use vpxenc for encoding video")
        self.add_option("--gecko-profiler-addon-dir", action="store",
                        dest="gecko_profiler_addon_dir", default=GECKO_PROFILER_ADDON_DIR,
                        help="Path to gecko profiler addon (default: %default)")

    def parse_args(self):
        (options, args) = CaptureOptionParser.parse_args(self)

        # parse out environment variables
        dict = {}
        for kv in options.extra_env_vars.split():
            (var, _, val) = kv.partition("=")
            dict[var] = val
        options.extra_env_vars = dict

        # parse out preferences
        try:
            dict = json.loads(options.extra_prefs)
            options.extra_prefs = dict
        except ValueError:
            self.error("Error processing extra preferences: not valid JSON!")
            raise

        if options.devicetype == 'b2g' and options.sync_time and \
                not options.wifi_settings_file:
            raise self.error('You must specify a WiFi settings file when '
                             'using B2G and sync time.')

        # if we're using a decklink card and have not specified the
        # resolution, try to get it by looking at the device model and
        # our default for it
        if not options.mode and options.capture_device == 'decklink':
            device_prefs = getDevicePrefs(options)
            device = getDevice(**device_prefs)
            options.mode = device.hdmiResolution

        return (options, args)
