# Copyright 2015 Cisco Systems, Inc.
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
from ucsc_apis.admin.syslog import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_syslog_local_console_enable():
    mo = syslog_local_console_enable(handle, severity="alerts")
    assert_equal(mo.severity, "alerts")


def test_002_syslog_local_monitor_enable():
    mo = syslog_local_monitor_enable(handle, severity="emergencies")
    assert_equal(mo.severity, "emergencies")


def test_003_syslog_local_file_enable():
    mo = syslog_local_file_enable(handle, name="test_syslog", size="10000")
    assert_equal(mo.size, "10000")


def test_004_syslog_remote_enable():
    mo = syslog_remote_enable(handle, name="primary", hostname="192.168.1.2",
                              forwarding_facility="local3")
    assert_equal(mo.forwarding_facility, "local3")


def test_005_syslog_source():
    mo = syslog_source(handle, faults="enabled", events="enabled")
    assert_equal(mo.faults, "enabled")


def test_006_remote_disable():
    mo = syslog_remote_disable(handle, name="primary")
    assert_equal(mo.admin_state, "disabled")


def test_007_local_monitor_disable():
    mo = syslog_local_monitor_disable(handle)
    assert_equal(mo.admin_state, "disabled")


def test_008_local_file_disable():
    mo = syslog_local_file_disable(handle)
    assert_equal(mo.admin_state, "disabled")


def test_009_local_console_disable():
    mo = syslog_local_console_disable(handle)
    assert_equal(mo.admin_state, "disabled")
