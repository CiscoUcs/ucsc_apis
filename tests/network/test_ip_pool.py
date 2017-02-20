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
from ucsc_apis.network.ip_pool import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_ip_pool_create():
    ip_pool_create(handle, name="test_ip_pool", descr="testing ip pool")
    found = ip_pool_exists(handle, name="test_ip_pool")[0]
    assert_equal(found, True)


def test_002_ip_block_add():
    ip_block_add(handle, "test_ip_pool", "1.1.1.1", "1.1.1.10",
                 "255.255.255.0", "1.1.1.254")
    found = ip_pool_exists(handle, name="test_ip_pool", r_from="1.1.1.1",
                           to="1.1.1.10", subnet="255.255.255.0",
                           def_gw="1.1.1.254")[0]
    assert_equal(found, True)


def test_003_ip_pool_remove():
    ip_pool_remove(handle, name="test_ip_pool")
    found = ip_pool_exists(handle, name="test_ip_pool")[0]
    assert_equal(found, False)
