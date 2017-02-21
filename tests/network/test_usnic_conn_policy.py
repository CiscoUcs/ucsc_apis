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
from ucsc_apis.network.usnic_conn_policy import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_usnic_conn_policy_create():
    usnic_conn_policy_create(
        handle, name="test_usnic_pol", descr="testing usnic")
    found = usnic_conn_policy_exists(handle, name="test_usnic_pol")[0]
    assert_equal(found, True)
    mo = usnic_conn_policy_create(
        handle, name="test_usnic_pol", usnic_count="32")
    assert_equal(mo.usnic_count, "32")


def test_002_usnic_conn_policy_delete():
    usnic_conn_policy_delete(handle, name="test_usnic_pol")
    found = usnic_conn_policy_exists(handle, name="test_usnic_pol")[0]
    assert_equal(found, False)
