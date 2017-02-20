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
from ucsc_apis.admin.timezone import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_timezone_set():
    mo = time_zone_set(handle, timezone="Asia/Manila")
    assert_equal(mo.timezone, "Asia/Manila")


def test_002_ntp_server_add():
    ntp_server_add(handle, name="192.168.1.1")
    found = ntp_server_exists(handle, name="192.168.1.1")[0]
    assert_equal(found, True)


def test_003_ntp_server_remove():
    ntp_server_remove(handle, name="192.168.1.1")
    found = ntp_server_exists(handle, name="192.168.1.1")[0]
    assert_equal(found, False)
