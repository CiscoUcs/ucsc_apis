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
from ucsc_apis.admin.radius import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_radius_provider_create():
    radius_provider_create(handle, name="test_radius_prov",
                           auth_port="320", timeout="10")
    found = radius_provider_exists(handle, name="test_radius_prov",
                                   auth_port="320")[0]
    assert_equal(found, True)


def test_002_radius_provider_modify():
    mo = radius_provider_modify(handle, name="test_radius_prov", timeout="5")
    assert_equal(mo.timeout, "5")


def test_003_radius_provider_group_create():
    radius_provider_group_create(handle, name="test_prov_grp")
    found = radius_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, True)


def test_004_radius_provider_group_add_provider():
    radius_provider_group_add_provider(
        handle, group_name="test_prov_grp", name="test_radius_prov")
    found = radius_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_radius_prov")[0]
    assert_equal(found, True)


def test_005_radius_provider_group_modify_provider():
    mo = radius_provider_group_modify_provider(
        handle, group_name="test_prov_grp", name="test_radius_prov",
        order="2")
    assert_equal(mo.order, "2")


def test_006_radius_provider_group_remove_provider():
    radius_provider_group_remove_provider(
        handle, group_name="test_prov_grp", name="test_radius_prov")
    found = radius_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_radius_prov")[0]
    assert_equal(found, False)


def test_007_radius_provider_group_delete():
    radius_provider_group_delete(handle, name="test_prov_grp")
    found = radius_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, False)


def test_008_radius_provider_delete():
    radius_provider_delete(handle, name="test_radius_prov")
    found = radius_provider_exists(handle, name="test_radius_prov")[0]
    assert_equal(found, False)
