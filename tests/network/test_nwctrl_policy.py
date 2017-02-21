# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..connection.info import custom_setup, custom_teardown
from nose.tools import *
from ucsc_apis.network.nwctrl_policy import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_nwctrl_policy_create():
    nwctrl_policy_create(handle, name="test_nwctrl_pol", descr="testing nwctr",
                         cdp="enabled", uplink_fail_action="warning")
    found = nwctrl_policy_exists(handle, name="test_nwctrl_pol", cdp="enabled",
                                 uplink_fail_action="warning")[0]
    assert_equal(found, True)


def test_002_nwctrl_policy_modify():
    nwctrl_policy_create(handle, name="test_nwctrl_pol",
                         cdp="disabled", forge="deny")
    mo = nwctrl_policy_get(handle, name="test_nwctrl_pol")
    assert_equal(mo.cdp, "disabled")


def test_003_nwctrl_policy_delete():
    nwctrl_policy_delete(handle, name="test_nwctrl_pol")
    found = nwctrl_policy_exists(handle, name="test_nwctrl_pol")[0]
    assert_equal(found, False)
