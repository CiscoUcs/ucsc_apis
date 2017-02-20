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
from ucsc_apis.network.mac_pool import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_mac_pool_create():
    mac_pool_create(handle, name="test_mac_pool", descr="testing macpool",
                    r_from="00:25:B5:00:00:04", to="00:25:B5:00:00:06")
    found = mac_pool_exists(handle, name="test_mac_pool",
                            r_from="00:25:B5:00:00:04",
                            to="00:25:B5:00:00:06")[0]
    assert_equal(found, True)


def test_002_mac_pool_remove():
    mac_pool_remove(handle, name="test_mac_pool")
    found = mac_pool_exists(handle, name="test_mac_pool")[0]
    assert_equal(found, False)
