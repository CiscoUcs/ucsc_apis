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
from ucsc_apis.admin.ldap import *

handle = None


def setup():
    global handle
    handle = custom_setup()


def teardown():
    custom_teardown(handle)


def test_001_ldap_provider_create():

    ldap_provider_create(handle, name="test_ldap_prov", port="320", order="3")
    found = ldap_provider_exists(handle, name="test_ldap_prov", port="320",
                                 order="3")[0]
    assert_equal(found, True)


def test_002_ldap_provider_modify():
    mo = ldap_provider_modify(handle, name="test_ldap_prov", enable_ssl="yes")
    assert_equal(mo.enable_ssl, "yes")


def test_003_ldap_provider_configure_rules():
    mo = ldap_provider_configure_group_rules(
            handle,
            ldap_provider_name="test_ldap_prov", authorization="enable")
    assert_equal(mo.authorization, "enable")


def test_004_ldap_group_map_create():
    ldap_group_map_create(handle, name="test_ldap_grp_map")
    found = ldap_group_map_exists(handle, name="test_ldap_grp_map")[0]
    assert_equal(found, True)


def test_005_ldap_group_map_add_role():
    ldap_group_map_add_role(
        handle, ldap_group_map_name="test_ldap_grp_map", name="storage")
    found = ldap_group_map_role_exists(
            handle,
            ldap_group_map_name="test_ldap_grp_map", name="storage")[0]
    assert_equal(found, True)


def test_006_ldap_provider_group_create():
    ldap_provider_group_create(handle, name="test_prov_grp")
    found = ldap_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, True)


def test_007_ldap_provider_group_add_provider():
    ldap_provider_group_add_provider(
        handle, group_name="test_prov_grp", name="test_ldap_prov")
    found = ldap_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_ldap_prov")[0]
    assert_equal(found, True)


def test_008_ldap_provider_group_modify_provider():
    mo = ldap_provider_group_modify_provider(
        handle, group_name="test_prov_grp", name="test_ldap_prov",
        order="2")
    assert_equal(mo.order, "2")


def test_009_ldap_provider_group_remove_provider():
    ldap_provider_group_remove_provider(
        handle, group_name="test_prov_grp", name="test_ldap_prov")
    found = ldap_provider_group_provider_exists(
            handle,
            group_name="test_prov_grp", name="test_ldap_prov")[0]
    assert_equal(found, False)


def test_010_ldap_provider_group_delete():
    ldap_provider_group_delete(handle, name="test_prov_grp")
    found = ldap_provider_group_exists(handle, name="test_prov_grp")[0]
    assert_equal(found, False)


def test_011_ldap_group_map_remove_role():
    ldap_group_map_remove_role(
        handle, ldap_group_map_name="test_ldap_grp_map", name="storage")
    found = ldap_group_map_role_exists(
            handle,
            ldap_group_map_name="test_ldap_grp_map", name="storage")[0]
    assert_equal(found, False)


def test_012_ldap_group_map_delete():
    ldap_group_map_delete(handle, name="test_ldap_grp_map")
    found = ldap_group_map_exists(handle, name="test_ldap_grp_map")[0]
    assert_equal(found, False)


def test_013_ldap_provider_delete():
    ldap_provider_delete(handle, name="test_ldap_prov")
    found = ldap_provider_exists(handle, name="test_ldap_prov")[0]
    assert_equal(found, False)
