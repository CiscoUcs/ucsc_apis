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
from ucsc_apis.admin.snmp import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_snmp_enable():
    mo = snmp_enable(handle, community="public", sys_contact="+001-12345678")
    assert_equal(mo.sys_contact, "+001-12345678")


def test_002_snmp_trap_add():
    snmp_trap_add(handle, hostname="3.3.3.3", community="public")
    found = snmp_trap_exists(handle, hostname="3.3.3.3")[0]
    assert_equal(found, True)


def test_003_snmp_trap_modify():
    mo = snmp_trap_modify(handle, hostname="3.3.3.3", version="v3")
    assert_equal(mo.version, "v3")


def test_004_snmp_user_add():
    snmp_user_add(handle, name="usr_snmp",
                  pwd="pwd#*22345", privpwd="pwd#*3456")
    found = snmp_user_exists(handle, name="usr_snmp")[0]
    assert_equal(found, True)


def test_005_snmp_user_modify():
    mo = snmp_user_modify(handle, name="usr_snmp", auth="sha")
    assert_equal(mo.auth, "sha")


def test_006_snmp_user_remove():
    snmp_user_remove(handle, name="usr_snmp")
    found = snmp_user_exists(handle, name="usr_snmp")[0]
    assert_equal(found, False)


def test_007_snmp_trap_remove():
    snmp_trap_remove(handle, hostname="3.3.3.3")
    found = snmp_trap_exists(handle, hostname="3.3.3.3")[0]
    assert_equal(found, False)


def test_008_snmp_trap_remove():
    mo = snmp_disable(handle)
    assert_equal(mo.admin_state, "disabled")
