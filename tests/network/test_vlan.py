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
from ucsc_apis.network.vlan import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_vlan_create():
    vlan_create(handle, name="test_vlan_create", id="560",
                sharing="isolated")
    found = vlan_exists(handle, name="test_vlan_create", id="560",
                        sharing="isolated")[0]
    assert_equal(found, True)
    vlan_create(handle, name="test_appl_vlan", id="660", vlan_type="appliance",
                sharing="community")
    found = vlan_exists(handle, name="test_appl_vlan", id="660",
                        vlan_type="appliance", sharing="community")[0]
    assert_equal(found, True)


def test_002_vlan_modify():
    mo = vlan_create(handle, name="test_vlan_create", id="560",
                     sharing="community")
    assert_equal(mo.sharing, "community")


def test_003_vlan_delete():
    vlan_delete(handle, name="test_vlan_create")
    found = vlan_exists(handle, name="test_vlan_create")[0]
    assert_equal(found, False)
    vlan_delete(handle, name="test_appl_vlan", vlan_type="appliance")
    found = vlan_exists(handle, name="test_appl_vlan",
                        vlan_type="appliance")[0]
    assert_equal(found, False)
