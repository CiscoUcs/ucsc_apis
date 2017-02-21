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
from ucsc_apis.network.qos import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_qos_policy_add():
    qos_policy_add(handle, name="test_qos_pol", descr="testing qos",
                   host_control="full", prio="platinum")
    found = qos_policy_exists(handle, name="test_qos_pol", host_control="full",
                              prio="platinum")[0]
    assert_equal(found, True)


def test_002_qos_policy_remove():
    qos_policy_remove(handle, name="test_qos_pol")
    found = qos_policy_exists(handle, name="test_qos_pol")[0]
    assert_equal(found, False)
