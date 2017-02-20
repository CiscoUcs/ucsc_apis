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
from ucsc_apis.network.mcast_policy import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_mcast_policy_create():
    mcast_policy_create(handle, name="test_mcast_pol", descr="testing mcast",
                        querier_ip_addr="10.10.10.1", querier_state="enabled")
    found = mcast_policy_exists(handle, name="test_mcast_pol",
                                querier_ip_addr="10.10.10.1",
                                querier_state="enabled")[0]
    assert_equal(found, True)


def test_002_mcast_policy_delete():
    mcast_policy_delete(handle, name="test_mcast_pol")
    found = mcast_policy_exists(handle, name="test_mcast_pol")[0]
    assert_equal(found, False)
